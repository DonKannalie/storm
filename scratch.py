from storm.__main__ import get_storm_instance

config_file = '/home/sj/.ssh/config'

storm_ = get_storm_instance(config_file)

host = storm_.search_host("m1")
print(host)


#%%

res = [(0, '11'), (2, '22')]

for r in res:
    print(r[1])


#%%
#
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
