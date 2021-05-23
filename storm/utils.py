# -*- coding: utf-8 -*-

import os
import subprocess as sp
from termcolor import colored
import sys

from defaults import col_dict


def fixed_width(text, size):
    text_width = len(text)
    if size > text_width:
        for _ in range(text_width, size):
            text += " "

    return text


class Colors:
    def __init__(self):
        self.col_user = col_dict['col_user']
        self.col_host = col_dict['col_host']
        self.col_port = col_dict['col_port']
        self.default = col_dict['default']

    def _get_color(self, search_for, dict_type):
        for k, v in dict_type.items():
            if search_for.startswith(k):
                return v
        return self.default

    def user(self, search_for):
        return self._get_color(search_for=search_for, dict_type=self.col_user)

    def host(self, search_for):
        return self._get_color(search_for=search_for, dict_type=self.col_host)

    def port(self, search_for):
        for k, v in self.col_port.items():
            if search_for == k:
                return self.default
            else:
                return v


COLOR_CODES = [
    "\x1b[1m",
    "\x1b[37m",
    "\x1b[0m",
    "\x1b[32m",
    "\x1b[35m",
]


def get_formatted_message(message, format_type):
    # required for CLI test suite. see tests.py
    if 'TESTMODE' in os.environ and not isinstance(message, ValueError):
        for color_code in COLOR_CODES:
            message = message.replace(color_code, "")

        return "{0} {1}".format(format_type, message)

    format_typed = fixed_width(format_type, 8)
    all_message = ""
    message = " %s" % message

    if format_type == 'error':
        all_message = colored(format_typed.upper(), 'red', attrs=["bold", ])
    elif format_type == 'success':
        all_message = colored(format_typed.upper(), 'green', attrs=["bold", ])

    return all_message + message
