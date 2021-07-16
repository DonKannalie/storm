#!/usr/bin/python
# -*- coding: utf-8 -*-
# TODO: add autocomplete https://github.com/kislyuk/argcomplete

import builtins
import platform  # For getting the operating system name
import colorama
import subprocess
import re
import json
import click
from pathlib import Path
from iterfzf import iterfzf
from typing import Iterable
import sys
import six
from storm import Storm
from storm.parsers.ssh_uri_parser import parse
from storm.utils_new import HostColors, colored
# from storm.kommandr import *
from collections.abc import Sequence
from storm.defaults import get_default
from storm import __version__
from storm.ssh_custom import SSH
from storm.check_server import get_server_info

colorama.init()

col = HostColors()


class InvalidValueError(Exception):
    """Raised on invalid value exception."""

    def __init__(self):
        self.message = 'invalid value: "@" cannot be used in name.'
        super().__init__()


def get_storm_instance(config_file=None):
    return Storm(config_file)


def get_aliases(param):
    config = Path('~').expanduser().joinpath('.config/stormssh/config')

    with open(config, 'r') as c:
        conf = json.loads(c.read())
    aliases = [param]
    for al in conf['aliases'][param]:
        aliases.append(al)
    return aliases


def cprint(msg, type_=''):
    type_dict = {
        "": "white",
        "error": "red",
        "success": "green",
        "info": "cyan"
    }
    click.echo(click.style(msg, fg=type_dict.get(type_)))


def ping(host_ip, n=None):
    """
    Returns True if host responds to a ping request
    """

    def eval_ping_response(ping_result):
        print(ping_result)
        print(type(ping_result))
        xxx'expected string or bytes-like object'
        packets = re.search(r'.*[P|p]ackets:? (.*)', ping_result).group(0)
        received = re.search(r'\d?\s[R|r]eceived(\s=\s\d)?', packets).group(0)
        rec = re.search(r'\d', received).group(0)
        if int(rec) == 0:
            return False
        else:
            return True

    n = 1 if n is None else n
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = f"ping {param} {str(n)} {host_ip}"
    out = subprocess.getstatusoutput(cmd)
    return eval_ping_response(out)


    # if int(rec) == 0:
    #     cprint(f"host: {name} ({ip})", 'error')
    # else:
    #     cprint(f"host: {name} ({ip})", 'success')


def ssh_copy_id(name):
    cmd = f'ssh-copy-id {name}'
    print(platform.system().lower())
    if platform.system().lower() == 'windows':
        cmd = f'type %USERPROFILE%\\.ssh\\id_rsa.pub | ssh {name} '
        cmd += '"mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && cat >> ~/.ssh/authorized_keys;"'
    return subprocess.check_output(cmd, shell=True)


@click.group('cli')
def cli():
    """
    Storm control ssh
    """


@cli.command()
def version():
    """
    prints the working storm(ssh) version.
    """
    cprint(__version__, 'info')


@cli.command('list')
@click.argument('name', nargs=-1, default=None)
def list_items(name, config=None):
    """
    Lists all hosts from ssh config.
    """
    storm_ = get_storm_instance(config)
    lastarg = sys.argv[-1]

    aliases = get_aliases('list')

    try:
        result = ""
        result_stack = ""

        padding = storm_.get_padding()

        if lastarg in aliases:
            result = colored('Listing entries:', 'cyan', attrs=["bold", ]) + "\n"
            entry_list = storm_.list_entries(True)
        else:
            result = colored(f'Listing entries filterd by {lastarg}', 'cyan', attrs=["bold", ]) + "\n"
            entry_list = storm_.list_entries(True, search=lastarg)

        # print(entry_list)
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

                        if key not in ["user", "hostname", "port"]:
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
        cprint(result)
    except Exception as error:
        cprint(error, 'error')
        sys.exit(1)


@cli.command('add')
@click.argument('name')
@click.argument('connection_uri')
@click.option('--id_file', '-i', default="", help="Identity file")
@click.option('--options', '-o', default=None, multiple=True, help="ssh options")
def add(name, connection_uri, id_file="", options=None, config=None):
    """
    Adds a new entry to sshconfig.
    Runs ssh-copy-id on new host afterwards.
    """
    options = [i for i in options]

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

        storm_.add_entry(name, host, user, port, id_file, options)

        try:
            if ping(host):
                ssh_copy_id(name)
            else:
                cprint(f'Could not add ssh key to host {name}, \nThe host is not reachable', 'error')
            cprint(f'ssh key added to host {name}', 'success')
        except Exception as error:
            cprint(str(error), 'error')
            sys.exit(1)

        cprint(f"\"{name}\" added to your ssh config. "
               f"\nyou can connect to it by typing ssh {name}", 'success')

    except ValueError as error:
        cprint(str(error), 'error')
        sys.exit(1)


@cli.command('delete')
@click.argument('name')
def delete(name, config=None):
    """
    Deletes a single host by name.
    """
    storm_ = get_storm_instance(config)

    try:
        storm_.delete_entry(name)
        cprint(f'hostname \"{name}\" deleted successfully.', 'success')
    except ValueError as error:
        cprint(error, 'error')
        sys.exit(1)


@cli.command('edit')
@click.argument('name')
@click.argument('connection_uri')
@click.option('--id_file', '-i', default="", help="Identity file")
@click.option('--options', '-o', default=None, multiple=True, help="ssh options")
def edit(name, connection_uri, id_file="", options=None, config=None):
    """
    Edits the related entry in ssh config.
    """
    options = [i for i in options]

    storm_ = get_storm_instance(config)

    try:
        if ',' in name:
            name = " ".join(name.split(","))

        user, host, port = parse(
            connection_uri,
            user=get_default("user", storm_.defaults),
            port=get_default("port", storm_.defaults)
        )
        storm_.edit_entry(name, host, user, port, id_file, options)
        cprint(f'\"{name}\" updated successfully.', 'success')
    except ValueError as error:
        cprint(error, 'error')
        sys.exit(1)


# @cli.command('update')
# @click.argument('name')
# @click.argument('connection_uri')
# @click.argument('id_file', nargs=-1)
# @click.option('options', '-o', default=None)
# def update(name, connection_uri="", id_file="", options=None, config=None):
#     """
#     Enhanced version of the edit command featuring multiple
#     edits using regular expressions to match entries
#     """
#
#     if options is None:
#         o = []
#     storm_ = get_storm_instance(config)
#     settings = {}
#
#     if id_file != "":
#         settings['identityfile'] = id_file
#
#     for option in o:
#         k, v = option.split("=")
#         settings[k] = v
#
#     print(name)
#     print(**settings)
#
#     # try:
#     #     storm_.update_entry(name, **settings)
#     #     cprint(f'\"{name}\" updated successfully.', 'success')
#     # except ValueError as error:
#     #     cprint(error, 'error')
#     #     sys.exit(1)


# @cli.command('search')
# @click.argument('name', default=None)
# def search(name, config=None):
#     """
#     Searches entries by given search text.
#     """
#     storm_ = get_storm_instance(config)
#     # aliases = get_aliases('search')
#     name = name[0]
#     try:
#         results = storm_.search_host(name)
#
#         if len(results) == 0:
#             print('no results found.')
#
#         if len(results) > 0:
#             message = ''
#             message += "".join(results)
#             print(message)
#     except Exception as error:
#         cprint(str(error), 'error')
#         sys.exit(1)


if __name__ == '__main__':
    cli()
