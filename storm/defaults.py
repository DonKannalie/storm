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
        "ping": ["p"],
        "wake": ["w", "wol"]
    },
    "mac": {
        "dummy": "12:12:12:12:12:12"
    }
}

# COLOR = {
#     # styles
#     'bold': ['\033[1m', '\033[22m'],
#     'italic': ['\033[3m', '\033[23m'],
#     'underline': ['\033[4m', '\033[24m'],
#     'inverse': ['\033[7m', '\033[27m'],
#     # grayscale
#     'white': ['\033[37m', '\033[39m'],
#     'grey': ['\033[90m', '\033[39m'],
#     'black': ['\033[30m', '\033[39m'],
#     # colors
#     'blue': ['\033[34m', '\033[39m'],
#     'cyan': ['\033[36m', '\033[39m'],
#     'green': ['\033[32m', '\033[39m'],
#     'magenta': ['\033[35m', '\033[39m'],
#     'red': ['\033[31m', '\033[39m'],
#     'yellow': ['\033[33m', '\033[39m'],
# }


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
