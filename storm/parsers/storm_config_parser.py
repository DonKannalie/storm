# -*- coding: utf-8 -*-

from pathlib import Path
from storm.utils import get_formatted_message
from storm.defaults import CONFIG_DATA
import json
import sys

config_root = Path.home().joinpath(".config/stormssh")
config_file = config_root.joinpath("config")


def create_config():
    print(get_formatted_message("StormSSH: Config file not found!", 'error'), file=sys.stderr)
    config_root.mkdir(exist_ok=True)
    with open(config_file, 'w') as cf:
        json.dump(CONFIG_DATA, cf, indent=4)
    if config_file.exists():
        print(get_formatted_message("StormSSH: Config file created: %s." % config_file, 'success'), file=sys.stderr)


def get_storm_config():
    if config_file.exists():
        try:
            config_data = json.loads(open(config_file).read())
            return config_data
        except Exception as error:
            print(get_formatted_message("StormSSH: Failure to load %s." % config_file, 'error'), file=sys.stderr)
    else:
        create_config()

    return {}
