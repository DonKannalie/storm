# -*- coding: utf-8 -*-

from os.path import expanduser
from os.path import exists
from os.path import join
from os import makedirs
import json


def get_storm_config():
    config_file = join(expanduser("~/.config/stormssh"), "config")

    if exists(config_file):
        try:
            config_data = json.loads(open(config_file).read())
            return config_data

        except Exception as error:
            pass
    else:
        makedirs(expanduser("~/.config/stormssh"), exist_ok=True)
    return {}

