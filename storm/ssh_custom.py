import os
import paramiko

from storm import interactive

# from getpass import getpass


class SSH:

    def __init__(self, server, username=None, port=None, identity_file=None):
        self.server = server

        if username is None:
            self.username = 'root'
        else:
            self.username = username

        if port is None:
            self.port = 22
        else:
            self.port = port

        if identity_file is None:
            self.identity_file = os.path.join("~", ".ssh", "id_rsa")
        else:
            self.identity_file = identity_file

        self.key = paramiko.RSAKey.from_private_key_file(os.path.expanduser(self.identity_file))
        self.sss = None
        self.sftp = None
        self.timeout = 5

    def open(self):
        self.sss = paramiko.SSHClient()
        self.sss.load_system_host_keys()
        self.sss.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.sss.connect(self.server, username=self.username, pkey=self.key, timeout=self.timeout)
        except paramiko.AuthenticationException:
            print("[-] Authentication Exception! ...")
            # return
            exit(1)
        except paramiko.SSHException:
            print("[-] SSH Exception! ...")
            # return
            exit(1)
        except Exception as err:
            print("[-] Exception!:", err)
            # return
            exit(1)
        return True

    def open_transport(self):
        if self.sss:
            transport = paramiko.Transport((self.server, self.port))
            transport.connect(username=self.username, pkey=self.key)
            self.sss._transport = transport

    def open_sftp(self):
        sftp = self.sss.open_sftp()
        return sftp

    def close(self):
        self.sss.close()
        try:
            self.sftp.close()
        except AttributeError:
            pass

    def download_file(self, remote_file, local_file):
        sftp = self.open_sftp()
        sftp.get(remote_file, local_file)

    def upload_file(self, local_file, remote_file):
        sftp = self.open_sftp()
        sftp.put(local_file, remote_file)

    def run_cmd(self, cmd):
        if self.sss:
            try:
                stdin, stdout, stderr = self.sss.exec_command(cmd)
                # if "sudo" in cmd:
                #     # pw = getpass(f"Enter password for server: {self.server} user: {self.username}")
                #     pw = input(f"Enter password for server: {self.server} user: {self.username}")
                #     stdin.write(pw)
                r_out, r_err = stdout.read(), stderr.read()
                # return r_out
                return r_out.decode()
            except AttributeError:
                print(f"Could not connect to host: '{self.server}' with user: '{self.username}'")

    def interactive(self):
        self.open_transport()
        channel = self.sss._transport.open_session()
        channel.get_pty()
        channel.invoke_shell()
        interactive.interactive_shell(channel)
