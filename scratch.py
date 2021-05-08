from importlib import reload
import storm

reload(storm)
import re
from storm import Storm
# from iterfzf import iterfzf
from storm.utils import get_formatted_message
from storm.__main__ import ping

config_file = '/home/sj/.ssh/config'

storm_ = Storm(config_file)

entries = storm_.host_list()

print(entries)
# res = iterfzf(entries)
import sys

# %%


res = 'beast >>> 10.161.11.52'
# res = ['beast >>> 10.161.11.52', 'cm2 >>> 172.18.1.32', 'g1 >>> 10.161.100.10']
# res = ''
if res is None or res is '':
    print("empty")
elif isinstance(res, str):
    print("str")
elif isinstance(res, list):
    print("list")

# %%
import subprocess
import platform


def ping(host_ip, n=None):
    """
    Returns True if host responds to a ping request
    """
    n = 1 if n is None else n
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = f"ping {param} {str(n)} {host_ip}"
    out = subprocess.getstatusoutput(cmd)
    return out



# name, ip = res.split('>>>')
# ip = res.split('>>>')[1]
# print(ip)

# for ip in ['10.161.11.51', 'google.com', '192.168.1.51']:
#     resp = ping(ip)
#     print(resp)
    # ping_response(resp)

# ping_list = []
# for entry in entries:
#     ping_list.append(entry['host'])

# print(ping_list)

# %%

resp = [(1,
         'PING 10.161.11.51 (10.161.11.51) 56(84) bytes of data.\n\n--- 10.161.11.51 ping statistics ---\n1 packets transmitted, 0 received, 100% packet loss, time 0ms\n'),
        (0,
         'PING google.com (172.217.23.238) 56(84) bytes of data.\n64 bytes from prg03s06-in-f238.1e100.net (172.217.23.238): icmp_seq=1 ttl=113 time=31.2 ms\n\n--- google.com ping statistics ---\n1 packets transmitted, 1 received, 0% packet loss, time 0ms\nrtt min/avg/max/mdev = 31.208/31.208/31.208/0.000 ms'),
        (0,
         'PING 192.168.1.51 (192.168.1.51) 56(84) bytes of data.\n64 bytes from 192.168.1.51: icmp_seq=1 ttl=127 time=0.185 ms\n\n--- 192.168.1.51 ping statistics ---\n1 packets transmitted, 1 received, 0% packet loss, time 0ms\nrtt min/avg/max/mdev = 0.185/0.185/0.185/0.000 ms'),
        (1,
         '\nPinging 10.161.11.51 with 32 bytes of data:\nRequest timed out.\n\nPing statistics for 10.161.11.51:\n    Packets: Sent = 1, Received = 0, Lost = 1 (100% loss),'),
        (0,
         '\nPinging google.com [172.217.23.238] with 32 bytes of data:\nReply from 172.217.23.238: bytes=32 time=31ms TTL=114\n\nPing statistics for 172.217.23.238:\n    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),\nApproximate round trip times in milli-seconds:\n    Minimum = 31ms, Maximum = 31ms, Average = 31ms'),
        (0,
         '\nPinging 192.168.1.51 with 32 bytes of data:\nReply from 192.168.1.51: bytes=32 time<1ms TTL=128\n\nPing statistics for 192.168.1.51:\n    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),\nApproximate round trip times in milli-seconds:\n    Minimum = 0ms, Maximum = 0ms, Average = 0ms')]


# for i in resp:
#     if isinstance(i, tuple)
#     print(type(i))
#

#%%
def ping_response(ping_result, name=None, ip=None):
    packets = re.search(r'.*[P|p]ackets:? (.*)', ping_result[1]).group(0)
    received = re.search(r'\d?\s[R|r]eceived(\s=\s\d)?', packets).group(0)
    rec = re.search(r'\d', received).group(0)
    if int(rec) == 0:
        print(get_formatted_message(f"host: {name} with {ip} not reached", 'error'), file=sys.stderr)
    else:
        print(get_formatted_message(f"host: {name} with {ip} reached", 'success'))

for selected in ['10.161.11.51', 'google.com', ['192.168.1.51', '192.168.1.81']]:
    if selected is None or selected == '':
        print(f"None selected", 'error')
    elif isinstance(selected, str):
        print("")

# for res in resp:
#     # print(res[1])
#     packets = re.search(r'.*[P|p]ackets:? (.*)', res[1]).group(0)
#     # print(packets)
#     received = re.search(r'\d?\s[R|r]eceived(\s=\s\d)?', packets).group(0)
#     # print(received.group(0))
#     rec = re.search(r'\d', received).group(0)


    # received = re.findall(r'')

    # failed = re.findall(r".*([U|u]nreachable).*", res[1], re.MULTILINE)

# %%
# import os
# import platform  # For getting the operating system name
# import subprocess  # For executing a shell command
# import re
#
# def ping(host, n=None):
#     """
#     Returns True if host responds to a ping request
#     """
#     n = 1 if n is None else n
#     param = "-n" if platform.system().lower() == "windows" else "-c"
#     cmd = f"ping {param} {str(n)} {host}"
#     print(cmd)
#     # cmd = ['ping', param, str(n), host]
#     need_sh = False if platform.system().lower() == "windows" else True
#     out = subprocess.getstatusoutput(cmd)
#     return out
#
#
# ips = ['192.168.1.51', '192.168.1.99']
#
# for ip in ips:
#     result = ping(ip, n=3)
#     print(result)
#     # if "Unreachable" in result:
#     #     print("not reached")
#     # else:
#     #     print("reached")
#
#
# # %%
# import re
#
# res_sh_pos = 'PING 192.168.1.51 (192.168.1.51) 56(84) bytes of data.\n64 bytes from 192.168.1.51: icmp_seq=1 ttl=127 time=0.206 ms\n\n--- 192.168.1.51 ping statistics ---\n1 packets transmitted, 1 received, 0% packet loss, time 0ms\nrtt min/avg/max/mdev = 0.206/0.206/0.206/0.000 ms'
#
# res_sh_neg = 'PING 192.168.1.99 (192.168.1.99) 56(84) bytes of data.\nFrom 192.168.1.51 icmp_seq=1 Destination Host Unreachable\n\n--- 192.168.1.99 ping statistics ---\n1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms\n'
#
# res_win_pos = '\nPinging 192.168.1.51 with 32 bytes of data:\nReply from 192.168.1.51: bytes=32 time<1ms TTL=128\n\nPing statistics for 192.168.1.51:\n    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),\nApproximate round trip times in milli-seconds:\n    Minimum = 0ms, Maximum = 0ms, Average = 0ms'
#
# res_win_neg = '\nPinging 192.168.1.99 with 32 bytes of data:\nReply from 192.168.1.51: Destination host unreachable.\n\nPing statistics for 192.168.1.99:\n    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),'
#
# ress = [res_sh_pos, res_sh_neg, res_win_pos, res_win_neg]
#
#
#
#
#
#
# #%%
#
# for res in ress:
#     result = {'status': False, 'sent': '', 'received': '', 'lost': '', 'loss': ''}
#     print("*" * 80)
#     # print(res)
#     failed = re.findall(r".*([U|u]nreachable).*", res, re.MULTILINE)
#
#
#     if failed:
#         result['status'] = False
#     else:
#         result['status'] = True
#
#     print(re.search('Sent = (\d+?),.*', res))
#
#
#
#     print(result)
#
#
#
#
# result = {'status': False, 'sent': '', 'received': '', 'lost': '', 'loss': ''}
#
# status = re.match(b'.*(unreachable).*', res)
# print(status)
# if status:
#     result['status'] = True
# else:
#     result['status'] = False
#
# res = res_neg
# packets = re.search(b'.*Packets: (.*)', res)
# sent = re.search(b'Sent = (\d+?),.*', packets.group(0))
# result['sent'] = sent.group(1).decode("utf-8")
#
# received = re.search(b'Sent = (\d+?),.*', packets.group(0))
# result['received'] = received.group(1).decode("utf-8")
#
# lost = re.search(b'Lost = (\d+?)\s.*', packets.group(0))
# result['lost'] = lost.group(1).decode("utf-8")
#
# loss = re.search(b'\((\d+?)%.*\)', packets.group(0))
# result['loss'] = loss.group(1).decode("utf-8")
#
# print(result)
#
# if result['status']:
#     print("reached")
# else:
#     print("not reached")
#
#
