# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import json

from operator import itemgetter
from shutil import copyfile
from pathlib import Path

import six
from wakeonlan import send_magic_packet

from .parsers.ssh_config_parser import ConfigParser
from .defaults import get_default

__version__ = '1.7.24'

ERRORS = {
    "already_in": "{0} is already in your sshconfig. "
                  "use storm edit or storm update to modify.",
    "not_found": "{0} doesn\'t exists in your sshconfig. "
                 "use storm add command to add.",
}

DELETED_SIGN = "DELETED"


class ItemExists(Exception):
    """Raised when item already in config"""

    def __init__(self, name):
        super().__init__(name)

    @property
    def msg(self):
        return self.args[0]

    # f"{name} is already in your sshconfig. \nUse storm edit or storm update to modify."


class Storm(object):

    def __init__(self, ssh_config_file=None):
        self.ssh_config = ConfigParser(ssh_config_file)
        self.ssh_config.load()
        self.defaults = self.ssh_config.defaults

    def add_entry(self, name, host, user, port, id_file, custom_options=None):
        if custom_options is None:
            custom_options = []

        if self.is_host_in(name):
            raise ValueError(ERRORS["already_in"].format(name))

        options = self.get_options(host, user, port, id_file, custom_options)

        self.ssh_config.add_host(name, options)
        self.ssh_config.write_to_ssh_config()

        return True

    def clone_entry(self, name, clone_name, keep_original=True):
        host = self.is_host_in(name, return_match=True)
        if not host:
            raise ValueError(ERRORS["not_found"].format(name))

        # check if an entry with the clone name already exists        
        if name == clone_name \
                or self.is_host_in(clone_name, return_match=True) is not None:
            raise ValueError(ERRORS["already_in"].format(clone_name))

        self.ssh_config.add_host(clone_name, host.get('options'))
        if not keep_original:
            self.ssh_config.delete_host(name)
        self.ssh_config.write_to_ssh_config()

        return True

    def edit_entry(self, name, host, user, port, id_file, custom_options=None):
        print(custom_options)
        if custom_options is None:
            custom_options = []

        if not self.is_host_in(name):
            raise ValueError(ERRORS["not_found"].format(name))

        options = self.get_options(host, user, port, id_file, custom_options)
        print(options)
        self.ssh_config.update_host(name, options, use_regex=False)
        self.ssh_config.write_to_ssh_config()

        return True

    def update_entry(self, name, **kwargs):
        if not self.is_host_in(name, regexp_match=True):
            raise ValueError(ERRORS["not_found"].format(name))

        self.ssh_config.update_host(name, kwargs, use_regex=True)
        self.ssh_config.write_to_ssh_config()

        return True

    def delete_entry(self, name):
        self.ssh_config.delete_host(name)
        self.ssh_config.write_to_ssh_config()

        return True

    def list_entries(self, order=False, only_servers=False, search=None):

        config_data = self.ssh_config.config_data

        if search is not None:
            config_data_ = []
            for i in config_data:
                if search in i.get("host"):
                    config_data_.append(i)
            config_data = config_data_

        # required for the web api.
        if only_servers:
            new_config_data = []
            for index, value in enumerate(config_data):
                if value.get("type") == 'entry' and value.get("host") != '*':
                    new_config_data.append(value)

            config_data = new_config_data

        if order:
            config_data = sorted(config_data, key=itemgetter("host"))
        return config_data

    def host_list(self):
        config_data = self.ssh_config.config_data

        host_list = []
        for host_entry in config_data:
            if host_entry.get("type") == 'entry' and host_entry.get("host") != '*':
                host_list.append(f"{host_entry.get('host')} >>> {host_entry.get('options').get('hostname')}")
        return host_list

    def delete_all_entries(self):
        self.ssh_config.delete_all_hosts()

        return True

    # def _search_host(self, search_string):
    #     return self.ssh_config.search_host(search_string)

    def search_host(self, search_string, exact_search=False):
        results = self.ssh_config.search_host(search_string, exact_search)
        formatted_results = []
        for host_entry in results:
            formatted_results.append("{0} >> {1}@{2} -p {3}\n".format(
                host_entry.get("host"),
                host_entry.get("options").get(
                    "user", get_default("user", self.defaults)
                ),
                host_entry.get("options").get(
                    "hostname", "[hostname_not_specified]"
                ),
                host_entry.get("options").get(
                    "port", get_default("port", self.defaults)
                ),
            ))

        return formatted_results

    def get_host_by_ip(self, search_string):
        ip = self.ssh_config.search_byip(search_string)
        if ip:
            ip_clean = ''.join(ip)
        else:
            ip_clean = 'unknown'
        return ip_clean

    def get_options(self, host, user, port, id_file, custom_options):
        options = {
            'hostname': host,
            'user': user,
            'port': port,
        }

        if id_file == DELETED_SIGN:
            options['deleted_fields'] = ["identityfile"]
        else:
            if id_file:
                options.update({'identityfile': id_file, })

        if len(custom_options) > 0:
            for custom_option in custom_options:
                if '=' in custom_option:
                    key, value = custom_option.split("=")
                    options.update({key.lower(): value, })

        options = self._quote_options(options)

        return options

    def is_host_in(self, host, return_match=False, regexp_match=False):
        for host_ in self.ssh_config.config_data:
            if host_.get("host") == host \
                    or (regexp_match and re.match(host, host_.get("host"))):
                return True if not return_match else host_
        return False if not return_match else None

    def backup(self, target_file):
        return copyfile(self.ssh_config.ssh_config_file, target_file)

    def _quote_options(self, options):
        keys_should_be_quoted = ["identityfile", ]
        for key in keys_should_be_quoted:
            if key in options:
                options[key] = '"{0}"'.format(options[key].strip('"'))

        return options

    def get_hostname(self, search_string, glob):
        glob = not glob
        results = self.ssh_config.search_host(search_string, exact_search=glob)
        formatted_results = []
        for host_entry in results:
            formatted_results.append("{0}".format(
                host_entry.get("options").get(
                    "hostname", "[hostname_not_specified]"
                )
            ))

        return formatted_results

    # def get_host(self, search_string, glob):
    #     glob = not glob
    #     results = self.ssh_config.search_host(search_string, exact_search=glob)
    #     formatted_results = []
    #     for host_entry in results:
    #         formatted_results.append("{0}".format(
    #             host_entry.get("options").get(
    #                 "hostname", "[hostname_not_specified]"
    #             )
    #         ))

    def get_padding(self):
        return self.ssh_config.get_max_length_host()

    def wake(self, name):
        # TODO: implement this properly!

        config = Path('~').expanduser().joinpath('.config/stormssh/config')

        with open(config, 'r') as c:
            conf = json.loads(c.read())

        mac_list = None
        try:
            mac_list = conf['mac']
        except KeyError:
            print(f"Could not find ~/.config/stormssh/maclist."
                  f"\nThis file is not automatically created."
                  f"\nSee 'storm --help' for more info")
            exit()
            # return
        [ip] = self.get_hostname(name, glob=False)
        mac_addr = None
        try:
            mac_addr = mac_list[name]
        except ValueError:
            print(f"No mac address for '{name}' fround")
            exit()
            # return

        if mac_addr and ip:
            print(f"WOL {ip} {mac_addr}")
            send_magic_packet(mac_addr, ip_address=ip)
        elif mac_addr:
            print(f"WOL {mac_addr}")
            send_magic_packet(mac_addr)
        else:
            print("DEBUG: formulate a appropriate message here")
