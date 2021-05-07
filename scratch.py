from storm.__main__ import get_storm_instance
from storm import Storm
from iterfzf import iterfzf

import tempfile
import os

from storm import __version__

print(__version__)

# config_file = '/home/sj/.ssh/config'
#
# storm_ = Storm(config_file)
#
# entries = storm_.list_entries()
# print(entries)
#
# ping_list = []
# for entry in entries:
#     ping_list.append(entry['host'])
#
# print(ping_list)
#
#
# iterfzf(ping_list)

#
# fzf = FzfPrompt()
# fzf.prompt(ping_list)

# from paramiko import SSHClient
# from scp import SCPClient
# from storm import Storm, get_default
# from pathlib import Path
# from storm.__main__ import get_storm_instance
#
#
# # use -c flag for copy-id
# # copy_cmd scp /path/to/file username@a:/path/to/destination
#
# print(Path('.').cwd())
#
#
# class StormTest(Storm):
#
#     def search_host_list(self, search_string, exact_search=False):
#         out = []
#         result = self.ssh_config.search_host(search_string, exact_search)
#         if result:
#             result = result[0]
#             out.append(result.get("host"))
#             out.append(result.get("options").get("user", get_default("user", self.defaults)))
#             out.append(result.get("options").get("hostname", "[hostname_not_specified]"))
#             out.append(result.get("options").get("port", get_default("port", self.defaults)))
#         return out
#
#     def copy_file(self, file):
#         print("copy_config")
#         scp.put(file)
#
#
# config_file = '/home/sj/.ssh/config'
#
# storm_ = StormTest(config_file)
# h = 'home-srv'
# result = storm_.search_host_list(h, exact_search=False)
# print(result)
#
#
#
# ssh = SSHClient()
# ssh.load_system_host_keys()
# ssh.connect('192.168.1.130')
# # ssh.connect(result[2])
#
# scp = SCPClient(ssh.get_transport())
#
# storm = StormTest()
#
# storm.copy_file('./dev/.tmux.config')
#
#
#
# # TODO: get bash completion with access token
#
# # ACCESS_TOKEN='1234567890abcdefghijk'
# # REPO_DOWNLOAD_URL=$(curl -u "${ACCESS_TOKEN}:" -s https://api.github.com/repos/owner-name/repo-name/releases/latest | \
# #   awk '/tag_name/ {print "https://api.github.com/repos/owner-name/repo-name/tarball/" substr($2, 2, length($2)-3) ""}'
# # )
# #
# # curl -u "${ACCESS_TOKEN}:" -LkSs "{$REPO_DOWNLOAD_URL}" -o - | tar xzf -
#
#
# # token='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'
# #
# #
# # curl "https://raw.github.com/org/dotfiles/dot_bashrc/file?login=DonKannalie&token=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"
# #
# # curl -H 'Authorization: token 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' \
# #   -H 'Accept: application/vnd.github.v3.raw' \
# #   -O \
# #   -L https://api.github.com/repos/DonKannalie/dotfiles/blob/master/dot_bashrc
