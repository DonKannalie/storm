#!/usr/bin/python
# -*- coding: utf-8 -*-
# TODO: add autocomplete https://github.com/kislyuk/argcomplete

from __future__ import print_function

import builtins
from storm import Storm
from storm.parsers.ssh_uri_parser import parse
from storm.utils import (get_formatted_message, colored)
from storm.kommandr import *
from storm.defaults import get_default
from storm import __version__

import platform  # For getting the operating system name
import colorama
import subprocess
import sys
import re
# from iterfzf import iterfzf


colorama.init()


class InvalidValueError(Exception):
    def __init__(self):
        self.message = 'invalid value: "@" cannot be used in name.'
        super().__init__(self.message)


def get_storm_instance(config_file=None):
    return Storm(config_file)


def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


def ssh_copy_id(name):
    cmd = f'ssh-copy-id {name}'
    if platform.system().lower() == 'windows':
        cmd = f'type %USERPROFILE%\\.ssh\\id_rsa.pub | ssh {name} '
        cmd += '"mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && cat >> ~/.ssh/authorized_keys;"'
    return subprocess.check_output(cmd, shell=True)


def ping(host_ip, n=None):
    """
    Returns True if host responds to a ping request
    """
    n = 1 if n is None else n
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = f"ping {param} {str(n)} {host_ip}"
    out = subprocess.getstatusoutput(cmd)
    return out


@command('version')
def version():
    """
    prints the working storm(ssh) version.
    """
    print(__version__)


@command('add')
def add(name, connection_uri, id_file="", o=None, config=None):
    """
    Adds a new entry to sshconfig.
    Runs ssh-copy-id on new host afterwards.
    """
    if o is None:
        o = []

    storm_ = get_storm_instance(config)

    try:

        # validate name
        if '@' in name:
            raise InvalidValueError

        user, host, port = parse(
            connection_uri,
            user=get_default("user", storm_.defaults),
            port=get_default("port", storm_.defaults)
        )

        storm_.add_entry(name, host, user, port, id_file, o)

        try:
            ssh_copy_id(name)

            print(
                get_formatted_message(
                    'ssh key added to host {0}".'.format(name),
                    'success')
            )
        except Exception as error:
            print(get_formatted_message(error, 'error'), file=sys.stderr)
            sys.exit(1)

        print(
            get_formatted_message(
                '{0} added to your ssh config. you can connect '
                'it by typing "ssh {0}".'.format(name),
                'success')
        )

    except ValueError as error:
        print(get_formatted_message(error, 'error'), file=sys.stderr)
        sys.exit(1)

    # _copy_id(name, config=None)


@command('clone')
def clone(name, clone_name, config=None):
    """
    Clone an entry to the sshconfig.
    """
    storm_ = get_storm_instance(config)

    try:

        # validate name
        if '@' in name:
            raise InvalidValueError

        storm_.clone_entry(name, clone_name)

        print(
            get_formatted_message(
                '{0} added to your ssh config. you can connect '
                'it by typing "ssh {0}".'.format(clone_name),
                'success')
        )

    except ValueError as error:
        print(get_formatted_message(error, 'error'), file=sys.stderr)
        sys.exit(1)


@command('move')
def move(name, entry_name, config=None):
    """
    Move an entry to the sshconfig.
    """
    storm_ = get_storm_instance(config)

    try:

        if '@' in name:
            raise InvalidValueError

        storm_.clone_entry(name, entry_name, keep_original=False)

        print(
            get_formatted_message(
                '{0} moved in ssh config. you can '
                'connect it by typing "ssh {0}".'.format(
                    entry_name
                ),
                'success')
        )

    except ValueError as error:
        print(get_formatted_message(error, 'error'), file=sys.stderr)
        sys.exit(1)


@command('edit')
def edit(name, connection_uri, id_file="", o=None, config=None):
    """
    Edits the related entry in ssh config.
    """
    if o is None:
        o = []
    storm_ = get_storm_instance(config)

    try:
        if ',' in name:
            name = " ".join(name.split(","))

        user, host, port = parse(
            connection_uri,
            user=get_default("user", storm_.defaults),
            port=get_default("port", storm_.defaults)
        )

        storm_.edit_entry(name, host, user, port, id_file, o)
        print(get_formatted_message(
            '"{0}" updated successfully.'.format(
                name
            ), 'success'))
    except ValueError as error:
        print(get_formatted_message(error, 'error'), file=sys.stderr)
        sys.exit(1)


@command('update')
def update(name, connection_uri="", id_file="", o=None, config=None):
    """
    Enhanced version of the edit command featuring multiple
    edits using regular expressions to match entries
    """
    if o is None:
        o = []
    storm_ = get_storm_instance(config)
    settings = {}

    if id_file != "":
        settings['identityfile'] = id_file

    for option in o:
        k, v = option.split("=")
        settings[k] = v

    try:
        storm_.update_entry(name, **settings)
        print(get_formatted_message(
            '"{0}" updated successfully.'.format(
                name
            ), 'success'))
    except ValueError as error:
        print(get_formatted_message(error, 'error'), file=sys.stderr)
        sys.exit(1)


@command('delete')
def delete(name, config=None):
    """
    Deletes a single host.
    """
    storm_ = get_storm_instance(config)

    try:
        storm_.delete_entry(name)
        print(
            get_formatted_message(
                'hostname "{0}" deleted successfully.'.format(name),
                'success')
        )
    except ValueError as error:
        print(get_formatted_message(error, 'error'), file=sys.stderr)
        sys.exit(1)


@command('list')
def list(config=None):
    """
    Lists all hosts from ssh config.
    """
    storm_ = get_storm_instance(config)

    try:
        result = colored('Listing entries:', 'white', attrs=["bold", ]) + "\n"
        result_stack = ""
        for host in storm_.list_entries(True):

            if host.get("type") == 'entry':
                if not host.get("host") == "*":

                    _user = host.get("options").get(
                        "user", get_default("user", storm_.defaults)
                    )
                    if _user == 'root':
                        _col = 'red'
                    else:
                        _col = 'white'

                    result += " {0}\t ->\t {1}@{2}:{3}".format(
                        colored(host["host"], 'green'),  # , attrs=["bold", ]

                        colored(_user, _col),

                        colored(host.get("options").get(
                            "hostname", "[hostname_not_specified]"
                        ), 'yellow'),

                        colored(host.get("options").get(
                            "port", get_default("port", storm_.defaults)
                        ), 'cyan')
                    )

                    extra = False
                    for key, value in six.iteritems(host.get("options")):

                        if not key in ["user", "hostname", "port"]:
                            if not extra:
                                custom_options = colored(
                                    '\t[custom options] ', 'white'
                                )
                                result += " {0}".format(custom_options)
                            extra = True

                            if isinstance(value, Sequence):
                                if isinstance(value, builtins.list):
                                    value = ",".join(value)

                            result += "{0}={1} ".format(key, value)
                    if extra:
                        result = result[0:-1]

                    result += "\n"  # \n
                else:
                    result_stack = colored(
                        "   (*) General options: \n", "green", attrs=["bold", ]
                    )
                    for key, value in six.iteritems(host.get("options")):
                        if isinstance(value, type([])):
                            result_stack += "\t  {0}: ".format(
                                colored(key, "magenta")
                            )
                            result_stack += ', '.join(value)
                            result_stack += "\n"
                        else:
                            result_stack += "\t  {0}: {1}\n".format(
                                colored(key, "magenta"),
                                value,
                            )
                    result_stack = result_stack[0:-1] + "\n"

        result += result_stack
        print(get_formatted_message(result, ""))
    except Exception as error:
        print(get_formatted_message(str(error), ''), file=sys.stderr)
        sys.exit(1)


@command('search')
def search(search_text, config=None):
    """
    Searches entries by given search text.
    """
    storm_ = get_storm_instance(config)

    try:
        results = storm_.search_host(search_text)
        if len(results) == 0:
            print('no results found.')

        if len(results) > 0:
            # message = 'Listing results for {0}:\n'.format(search_text)
            message = ''
            message += "".join(results)
            print(message)
    except Exception as error:
        print(get_formatted_message(str(error), 'error'), file=sys.stderr)
        sys.exit(1)


@command('delete_all')
def delete_all(config=None):
    """
    Deletes all hosts from ssh config.
    """
    storm_ = get_storm_instance(config)

    try:
        storm_.delete_all_entries()
        print(get_formatted_message('all entries deleted.', 'success'))
    except Exception as error:
        print(get_formatted_message(str(error), 'error'), file=sys.stderr)
        sys.exit(1)


@command('backup')
def backup(target_file, config=None):
    """
    Backups the main ssh configuration into target file.
    """
    storm_ = get_storm_instance(config)
    try:
        storm_.backup(target_file)
    except Exception as error:
        print(get_formatted_message(str(error), 'error'), file=sys.stderr)
        sys.exit(1)


# @command('web')
# @arg('port', nargs='?', default=9002, type=int)
# @arg('theme', nargs='?', default="modern", choices=['modern', 'black', 'storm'])
# @arg('debug', action='store_true', default=False)
# def web(port, debug=False, theme="modern", ssh_config=None):
#     """Starts the web UI."""
#     from storm import web as _web
#     _web.run(port, debug, theme, ssh_config)


@command('get-ip')
@arg('glob', action='store_true', default=False)
def get_ip(name, glob=False, con=False, config=None):
    """
    Get hostname/ip by name in ssh config (use --glob for glob search)
    """
    # TODO: add user@hostname connection output
    storm_ = get_storm_instance(config)

    hostname = storm_.get_hostname(name, glob=glob)

    if hostname and isinstance(hostname, list):
        for host in hostname:
            print(get_formatted_message(host, 'success'), file=sys.stderr)


@command('copy-id')
def copy_ids(name, config=None):
    """
    ssh-copy-id function for Unix/Windows
    """
    # storm_ = get_storm_instance(config)
    # if storm_.search_host(name, True):
    ssh_copy_id(name)


@command('ping')
# @arg('glob', action='store_true', default=False)
@arg('n', type=int, default=1)
def ping_host(name, n=None, config=None, glob=False):
    """
    ping host by ip
    """
    # if glob: search_host, show found hosts name and corr. ip

    storm_ = get_storm_instance(config)
    ips = storm_.get_hostname(name, glob=glob)
    if ips:
        print(f"Pinging host: {name} with {', '.join(ips)}")
        for ip in ips:
            output = ping(host_ip=ip, n=n)
            print(output)
            failed = re.findall(r".*([U|u]nreachable).*", output[1], re.MULTILINE)
            if failed:
                print(get_formatted_message(f"host: {name} with {ip} not reached", 'error'), file=sys.stderr)
            else:
                print(get_formatted_message(f"host: {name} with {ip} reached", 'success'), file=sys.stderr)
    else:
        print(get_formatted_message(f"host: {name} not found", 'error'), file=sys.stderr)
# def ping_host(name, n=None, config=None, glob=False):
#     """
#     ping host by ip
#     """
#     # if glob: search_host, show found hosts name and corr. ip
#
#     storm_ = get_storm_instance(config)
#     entries = storm_.list_entries()
#
#     ping_list = []
#     for entry in entries:
#         ping_list.append(entry['host'])
#
#     iterfzf(ping_list)




# TODO: add
# TODO: add create-config function; remove from parsers/get_storm_config()
# TODO: add add-alias function, etc.
# @command('storm-config')
# @arg('create', action='store_true', default=False)
# @arg('delete', action='store_true', default=False)
# def storm_config(create=False):
#     if create:
#         print("")

# TODO: add dotfile copy; use -c flag for  copy_ids


# if os.name == 'nt':
#     if process_exists('Rainmeter.exe'):
#         @command('refresh')
#         def refresh():
#             """
#             Creates/Refreshes Rainmeter config.
#             """
#             from storm.ssh_rainmeter import main as rainmeter
#             rainmeter()
#             print(get_formatted_message("Rainmeter config has been refreshed", 'success'))
# else:
#     @command('refresh')
#     def refresh():
#         """
#         Refresh conky config.
#         """
#         print(get_formatted_message("Conky config not implemented yet", 'error'))

if __name__ == '__main__':
    sys.exit(main())
