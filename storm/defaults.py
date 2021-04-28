# -*- coding: utf-8 -*-

import getpass

DEFAULT_PORT = 22
DEFAULT_USER = getpass.getuser()

CONFIG_DATA = {
    "aliases": {
        "add": ["create", "touch"],
        "move": ["mv"],
        "update": ["up"],
        "delete": ["rm"],
        "list": ["ls", "lst", "show"],
        "search": ["find"],
        "get-ip": ["ip", "gip"],
        "copy-id": ["cid"],
        "ping": ["p"]
    }
}


def get_default(key, defaults={}):
    if key == 'port':
        return defaults.get("port", DEFAULT_PORT)

    if key == 'user':
        return defaults.get("user", DEFAULT_USER)

    return defaults.get(key)
