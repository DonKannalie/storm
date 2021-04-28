# -*- coding: utf-8 -*-

from os.path import expanduser
from os.path import exists
from os.path import join
from os import makedirs
from os import getcwd
from storm.defaults import CONFIG_DATA
from pathlib import Path
import json


def get_storm_config():

    config_root = Path.home().joinpath(".config/stormssh")
    config_file = config_root.joinpath("config")

    if config_file.exists():
        try:
            config_data = json.loads(open(config_file).read())
            return config_data

        except Exception as error:
            pass
    else:
        print("StormSSH: Config file not found!")
        config_root.mkdir(exist_ok=True)
        config_file.touch()
        if config_file.exists():
            with open(config_file, 'w') as cf:
                json.dump(CONFIG_DATA, cf, indent=4)
            print("StormSSH: Config file created in %s." % config_root)
    return {}
