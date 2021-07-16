#!/usr/bin/python
# -*- coding: utf-8 -*-
# TODO: add autocomplete https://github.com/kislyuk/argcomplete

from __future__ import print_function

import builtins
import platform  # For getting the operating system name
import colorama
import subprocess
import re
import json

from pathlib import Path
from iterfzf import iterfzf
from typing import Iterable

from storm import Storm
from storm.parsers.ssh_uri_parser import parse
from storm.utils import (get_formatted_message, colored, Colors)
from storm.kommandr import *
from storm.defaults import get_default
from storm import __version__
from storm.ssh_custom import SSH
from storm.check_server import get_server_info

colorama.init()

col = Colors()


class InvalidValueError(Exception):
    """Raised on invalid value exception."""

    def __init__(self):
        self.message = 'invalid value: "@" cannot be used in name.'
        super().__init__()


def display(message, code_type):
    if type == 'error':
        print(get_formatted_message(message, code_type), file=sys.stderr)
    else:
        print(get_formatted_message(message, code_type))


def get_aliases(param):
    config = Path('~').expanduser().joinpath('.config/stormssh/config')

    with open(config, 'r') as c:
        conf = json.loads(c.read())
    aliases = [param]
    for al in conf['aliases'][param]:
        aliases.append(al)
    return aliases


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


def eval_ping_response(ping_result, name, ip):
    packets = re.search(r'.*[P|p]ackets:? (.*)', ping_result).group(0)
    received = re.search(r'\d?\s[R|r]eceived(\s=\s\d)?', packets).group(0)
    rec = re.search(r'\d', received).group(0)
    if int(rec) == 0:
        display(f"host: {name} ({ip})", 'error')
    else:
        display(f"host: {name} ({ip})", 'success')


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
            display(f'ssh key added to host {name}', 'success')
        except Exception as error:
            display(error, 'error')
            sys.exit(1)

        display(f'{name} added to your ssh config. '
                f'\nyou can connect it by typing ssh {name}', 'success')

    except ValueError as error:
        display(error, 'error')
        sys.exit(1)


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

        display(f'{clone_name} added to your ssh config. '
                f'\nyou can connect it by typing '
                f'\"ssh {clone_name}\".', 'success')

    except ValueError as error:
        display(error, 'error')
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

        display(f'{entry_name} moved in ssh config. '
                f'\nyou can connect it by typing '
                f'\"ssh {0}\".', 'success')

    except ValueError as error:
        display(error, 'error')
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
        display(f'\"{name}\" updated successfully.', 'success')
    except ValueError as error:
        display(error, 'error')
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
        display(f'\"{name}\" updated successfully.', 'success')
    except ValueError as error:
        display(error, 'error')
        sys.exit(1)


@command('delete')
def delete(name, config=None):
    """
    Deletes a single host.
    """
    storm_ = get_storm_instance(config)

    try:
        storm_.delete_entry(name)
        display(f'hostname \"{name}\" deleted successfully.', 'success')
    except ValueError as error:
        display(error, 'error')
        sys.exit(1)


@command('list')
@arg('name', nargs='*', default=None)
def list_items(name, config=None):
    """
    Lists all hosts from ssh config.
    """
    storm_ = get_storm_instance(config)
    lastarg = sys.argv[-1]

    aliases = get_aliases('list')

    try:
        result = colored('Listing entries:', 'white', attrs=["bold", ]) + "\n"
        result_stack = ""
        padding = storm_.get_padding()

        if lastarg in aliases:
            entry_list = storm_.list_entries(True)
        else:
            entry_list = storm_.list_entries(True, search=lastarg)
        for host in entry_list:

            if host.get("type") == 'entry':
                if not host.get("host") == "*":

                    _user = host.get("options").get(
                        "user", get_default("user", storm_.defaults)
                    )

                    _host = host.get("options").get(
                        "hostname", "[hostname_not_specified]"
                    )

                    _port = host.get("options").get(
                        "port", get_default("port", storm_.defaults)
                    )

                    result += f"{colored(host['host'].ljust(padding), 'green')}" \
                              f"\t->\t" \
                              f"{colored(_user, col.user(_user))}" \
                              f"{colored('@', 'green')}" \
                              f"{colored(_host, col.host(_host))}" \
                              f"{colored(':', 'green')}" \
                              f"{colored(_port, col.port(_port))}"

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
        display(result, "")
    except Exception as error:
        display(str(error), '')
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
            message = ''
            message += "".join(results)
            print(message)
    except Exception as error:
        display(str(error), 'error')
        sys.exit(1)


@command('delete_all')
def delete_all(config=None):
    """
    Deletes all hosts from ssh config.
    """
    storm_ = get_storm_instance(config)

    try:
        storm_.delete_all_entries()
        display('all entries deleted.', 'success')
    except Exception as error:
        display(str(error), 'error')
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
        display(str(error), 'error')
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
            print(host)


@command('copy-id')
def copy_ids(name, config=None):
    """
    ssh-copy-id function for Unix/Windows
    """
    # storm_ = get_storm_instance(config)
    # if storm_.search_host(name, True):
    ssh_copy_id(name)


@command('ping')
@arg('name', nargs='*', default=None)
@arg('n', type=int, default=1)
@arg('glob', action='store_true', default=False)
def ping_host(name, n=None, config=None, glob=True):
    """
    ping host by its ip
    """
    ## work-around for
    lastarg = sys.argv[-1]

    storm_ = get_storm_instance(config)
    aliases = get_aliases('ping')

    if lastarg in aliases:
        entries = storm_.host_list()
        selected = iterfzf(entries, multi=True)
        # TODO: refactor this bullshit redundancy
        if selected is None or selected == '':
            display(f"None selected", 'error')
            exit(0)
        elif isinstance(selected, str):
            name, ip = selected.split('>>>')
            name = name.strip()
            ip = ip.strip()
            res = ping(ip)
            eval_ping_response(res, name, ip)
        elif isinstance(selected, Iterable):
            for entry in selected:
                name, ip = entry.split('>>>')
                name = name.strip()
                res = ping(ip)
                if isinstance(res, tuple):
                    eval_ping_response(res[1], name, ip)
                else:
                    print("DEBUG: the value from ping was not returned as a tuple. Please investigate!")
    else:
        [name] = name
        ips = storm_.get_hostname(name, glob=glob)
        if ips:
            # print(f"Pinging host{'s' if len(ips) > 1 else ''}: {name} with {', '.join(ips)}")
            for ip in ips:
                res = ping(host_ip=ip, n=n)
                if isinstance(res, tuple):
                    name_resolved = storm_.get_host_by_ip(ip)
                    eval_ping_response(res[1], name_resolved, ip)
                else:
                    print("DEBUG: the value from ping was not returned as a tuple. Please investigate!")
        else:
            display(f"host: {name} not found", 'error')


@command('wake')
def wake_host(name, config=None):
    """
    Wake a host from the list specified in ~/.config/stormssh/config
    format json (watch the commas):
    <aliases>,
    "mac": {
        "host1": "mac1",
        "host2": "mac2"
    }
    <server>: <mac_address>
    "server": "xx:xx:xx:xx:xx:xx"
    """
    storm_ = get_storm_instance(config)
    storm_.wake(name)


@command('create-config')
def create_config():
    """
    Create storm config ~/.config/stormssh/config
    You can apply aliases here
    """
    from storm.parsers.storm_config_parser import create_storm_config
    create_storm_config()


@command('check')
def check_server(name, config=None):
    storm_ = get_storm_instance(config)
    # host = storm_.search_host(name, exact_search=True)
    entries = storm_.list_entries(search=name)

    # if entries and len(entries) == 1:
    if entries:
        for entry in entries:
            hostname = entry.get('options').get('hostname')
            user = entry.get('options').get('user')
            port = entry.get('options').get('port')
            ident_file = entry.get('options').get('identityfile')
            # print(ident_file)
            if ident_file:
                ident_file = ident_file[0]
            print(hostname, user, port, ident_file)
            sshc = SSH(hostname, user, port, ident_file)
            status = sshc.open()
            print("ssh status: ", status)
            if status:
                get_server_info(sshc)
            sshc.close()
    else:
        display(f"host: {name} not found", 'error')


# TODO: 'check' command: ssh command to host
# free -h
# uptime
# w or w --ip-addr
# cat /proc/net/tcp | wc -l
# optional: ps auxf

# TODO: add create-config function; remove from parsers/get_storm_config()
# TODO: add add-alias function, etc.
# @command('storm-config')
# @arg('create', action='store_true', default=False)
# @arg('delete', action='store_true', default=False)
# def storm_config(create=False):
#     if create:
#         print("")


# if os.name == 'nt':
#     if process_exists('Rainmeter.exe'):
#         @command('refresh')
#         def refresh():
#             """
#             Creates/Refreshes Rainmeter config.
#             """
#             from storm.ssh_rainmeter import main as rainmeter
#             rainmeter()
#             display("Rainmeter config has been refreshed", 'success')
# else:
#     @command('refresh')
#     def refresh():
#         """
#         Refresh conky config.
#         """
#         display("Conky config not implemented yet", 'error')

if __name__ == '__main__':
    sys.exit(main())
