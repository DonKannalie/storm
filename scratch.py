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


#%%

def ping_response(ping_result, name, ip):
    failed = re.findall(r".*([U|u]nreachable).*", ping_result[1], re.MULTILINE)
    if failed:
        print(get_formatted_message(f"host: {name} with {ip} not reached", 'error'), file=sys.stderr)
    else:
        print(get_formatted_message(f"host: {name} with {ip} reached", 'success'), file=sys.stderr)

# res = 'beast >>> 10.161.11.52'
res = ['beast >>> 10.161.11.52', 'cm2 >>> 172.18.1.32', 'g1 >>> 10.161.100.10']
# res = ''
if res is None or res is '':
    print("empty")
elif isinstance(res, str):
    print("str")
elif isinstance(res, list):
    print("list")


#%%

name, ip = res.split('>>>')
ip = res.split('>>>')[1]

resp = (1, 'PING 10.161.11.52 (10.161.11.52) 56(84) bytes of data.\n\n--- 10.161.11.52 ping statistics ---\n1 packets transmitted, 0 received, 100% packet loss, time 0ms\n')

ping_response(resp, name, ip)


# ping_list = []
# for entry in entries:
#     ping_list.append(entry['host'])

# print(ping_list)






#%%
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
