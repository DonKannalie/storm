from termcolor import colored
from storm.defaults import col_dict


class HostColors:
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
