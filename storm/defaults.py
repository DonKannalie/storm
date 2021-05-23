# -*- coding: utf-8 -*-

import getpass

DEFAULT_PORT = 22
DEFAULT_USER = getpass.getuser()

CONFIG_DATA = {
    "aliases": {
        "add": ["a", "create"],
        "move": ["mv"],
        "update": ["up"],
        "delete": ["rm"],
        "list": ["l", "ls"],
        "search": ["s", "find"],
        "get-ip": ["ip", "gip"],
        "copy-id": ["cid"],
        "ping": ["p"]
    }
}

col_dict = {
    "col_user": {'root': 'red', 'admin': 'red', 'VMUDOMAIN': 'magenta'},
    "col_host": {'10.161.': 'yellow', '172.': 'red'},
    "col_port": {'22': 'cyan'},
    "default": 'white'
}


def get_default(key, defaults={}):
    if key == 'port':
        return defaults.get("port", DEFAULT_PORT)

    if key == 'user':
        return defaults.get("user", DEFAULT_USER)

    return defaults.get(key)
