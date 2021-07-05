import os
import re

from pathlib import Path
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY, ORGMODE, MARKDOWN

from storm.utils import colored


def banner(txt):
    length = len(txt)
    print(colored("#", 'green') * (length + 6))
    print(f"{colored('##', 'green')} {colored(txt, 'cyan')} {colored('##', 'green')}")
    print(colored("#", 'green') * (length + 6))

def run_quick_info(ssh_connection):
    ...




def run_w(ssh_connection):
    output = ssh_connection.run_cmd('w -si')
    print(output)
    table = None
    uptime = None

    for i, r in enumerate(output.split("\n")):
        if i == 1:
            header = r.split(" ")
            while "" in header:
                header.remove("")
            # print(rows)
            if header:
                table = PrettyTable(header)
        if i > 1:
            row = r.split(" ")
            while "" in row:
                row.remove("")
            # print(vals)
            if row:
                table.add_row(row)

    table.align = "l"
    table.set_style(MARKDOWN)

    banner("USER ON SERVER:")
    print(table, "\n")


def run_m(ssh_connection):
    output = ssh_connection.run_cmd('free -ht')
    table = None
    max_row = 0
    for i, r in enumerate(output.split("\n")):
        # print(i, r)

        if i == 0:
            header = [""] + r.split()
            # print(header)
            max_row = len(header)
            if header:
                table = PrettyTable(header)
                # print(header)
        elif i >= 1:
            row = r.split()
            if row:
                while len(row) < max_row:
                    row.append("")
                # print(row)
                table.add_row(row)
    table.align = "l"
    table.set_style(MARKDOWN)

    banner("MEMORY:")
    print(table, "\n")


def run_m_short(ssh_connection):
    output = ssh_connection.run_cmd('free -ht')
    for i, r in enumerate(output.split("\n")):
        mem = r.split()
        if i > 0 and mem:
            txt = f"{mem[3]} / {mem[1]} ({mem[2]})"
            print(f"{mem[0]}\t {colored(txt, 'green')} (Free/Total (Used))")
    print("")


def run_io(ssh_connection):
    output = ssh_connection.run_cmd('iostat -d')
    table = None

    for i, r in enumerate(output.split("\n")):
        # print(i, r)
        if i == 2:
            header = r.split()
            # print(header)
            if header:
                table = PrettyTable(header)
        elif i >= 1:
            row = r.split()
            # print(row)
            if row and "loop" not in row[0]:
                table.add_row(row)
    table.align = "l"
    # table.set_style(ORGMODE)
    table.set_style(MARKDOWN)

    banner("IO-STAT:")
    print(table, "\n")


def run_info(ssh_connection):
    cpu_usage = ssh_connection.run_cmd(
        "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'")
    cpu_txt = f"{cpu_usage.strip()} %"

    kernel_release = ssh_connection.run_cmd('uname -r')
    kernel_name = ssh_connection.run_cmd('uname -s')
    kernel_version = ssh_connection.run_cmd('uname -v')
    node_name = ssh_connection.run_cmd('uname -n')
    node_machine = ssh_connection.run_cmd('uname -m')
    node_os = ssh_connection.run_cmd('uname -o')
    host_name = ssh_connection.run_cmd('hostname -f')
    host_ip = ssh_connection.run_cmd('hostname -i')

    header = ['Type', 'Info']
    table = PrettyTable(header)
    info = ['Node name', 'Node OS', 'Mode machine', 'Kernel name', 'Kernel release', 'Kernel version']
    info_type = [node_name, node_os, node_machine, kernel_name, kernel_release, kernel_version]
    for k, v in zip(info, info_type):
        # print([k, v])
        table.add_row([k, colored(v.strip(), 'green')])
    table.align = 'l'
    # table.set_style(MARKDOWN)
    banner(f"System Info: {host_name.strip()} ({host_ip.strip()})")
    uptime = ssh_connection.run_cmd('uptime -p')
    if uptime:
        print(f"UPTIME: {colored(uptime, 'cyan')}")
    print(table, "\n")
    print("CPU usage:", colored(cpu_txt, "green"))

    mem_info = ssh_connection.run_cmd('free -ht')
    for i, r in enumerate(mem_info.split("\n")):
        mem = r.split()
        if i > 0 and mem:
            txt = f"{mem[3]} / {mem[1]} ({mem[2]})"
            print(f"{mem[0]}\t {colored(txt, 'green')} (Free/Total (Used))")
    print("")


def run_network(ssh_connection):
    output = ssh_connection.run_cmd('ip a')
    banner("Network devices")
    # print(output)

    wan_ip = ssh_connection.run_cmd("curl -A curl -s https://api.ipify.org")
    if wan_ip:
        print(f"WAN IP: {colored(wan_ip.strip(), 'green')}")

    ip_route = ssh_connection.run_cmd("ip route | grep ^default'\s'via | head -1 | awk '{print$3}'")
    if ip_route:
        print(f"IP ROUTE: {colored(ip_route.strip(), 'green')}")

    host_dns = ssh_connection.run_cmd("cat /etc/resolv.conf | grep -i ^nameserver | cut -d ' ' -f2")
    if host_dns:
        print(f"DNS: {colored(host_dns.strip(), 'green')}")

    net_info = []
    net_country = ssh_connection.run_cmd("curl -A curl -s \"http://ip-api.com/line/?fields=country\"")
    if net_country:
        net_info.append(net_country.strip())

    net_zip = ssh_connection.run_cmd("curl -A curl -s \"http://ip-api.com/line/?fields=zip\"")
    if net_zip:
        net_info.append(net_zip.strip())

    net_city = ssh_connection.run_cmd("curl -A curl -s \"http://ip-api.com/line/?fields=city\"")
    if net_city:
        net_info.append(net_city.strip())

    net_isp = ssh_connection.run_cmd("curl -A curl -s \"http://ip-api.com/line/?fields=isp\"")
    if net_isp:
        net_info.append(net_isp.strip())

    if net_info:
        print("GEO info: ", colored(', '.join(net_info), 'green'))

    pattern_mac = r"([0-9a-f]{2}(?::[0-9a-f]{2}){5})"
    pattern_ip = r"(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?"
    pattern_state = r"state\s(\w+)\s"
    print("")
    for i, r in enumerate(output.split("\n")):

        dev = ''
        ip = ''
        mac = ''
        try:
            if re.search('^\d', str(r[0])):
                dev = f"{r.split()[0]} {r.split()[1]}"
                dev += f" {re.search(pattern_state, r)[1]}"
        except Exception:
            pass

        if re.search('^\s+inet\s', r):
            ip = [i for i in re.findall(pattern_ip, r) if '255' not in i]
        if re.search(pattern_mac, r):
            mac = [i for i in re.findall(pattern_mac, r) if i != 'ff:ff:ff:ff:ff:ff']

        out = ''
        if dev:
            print(dev.strip())
        if ip:
            ip_f = ip
            if "/" in ip[0]:
                ip_f = ip[0].split('/')[0]
            if ip_f == ssh_connection.server:
                print("\tIP:", colored(ip[0].strip(), 'green'), "(connected device)")
            else:
                print("\tIP:", colored(ip[0].strip(), 'green'))
        if mac:
            print("\tMac:", colored(mac[0].strip(), 'blue'))

    print("")


def short_status(ssh_connection):
    print()
    out = ssh_connection.upload_file('collect_server_info.sh', '/home/sj/collect_server_info.sh')
    out = ssh_connection.run_cmd('bash ~/collect_server_info.sh')
    ssh_connection.run_cmd('rm -f ~/collect_server_info.sh')

    server_info = {}

    for i in out.split("\n"):
        if i:
            key, val = i.split("=")
            if val:
                server_info[key] = [val][0]

    header = ['Type', 'Info']
    table = PrettyTable(header)
    for k, v in server_info.items():
        # print(k, v)
        table.add_row([k.replace("_", " ").upper(), colored(v.strip(), 'green')])

    table.align = 'l'
    print(table)

def get_server_info(ssh_connection):
    short_status(ssh_connection)
    # run_info(ssh_connection)
    # run_network(ssh_connection)
    # run_m(ssh_connection)
    # run_w(ssh_connection)
    # run_io(ssh_connection)

















# import re
#
# from prettytable import PrettyTable
# from prettytable import MSWORD_FRIENDLY, ORGMODE, MARKDOWN
#
# from storm.utils import colored
#
#
# def banner(txt):
#     length = len(txt)
#     print(colored("#", 'green') * (length + 6))
#     print(f"{colored('##', 'green')} {colored(txt, 'cyan')} {colored('##', 'green')}")
#     print(colored("#", 'green') * (length + 6))
#
#
# def run_w(ssh_connection):
#     output = ssh_connection.run_cmd('w')
#     table = None
#     uptime = None
#
#     for i, r in enumerate(output.split("\n")):
#         # if i == 0:
#         # uptime = r
#         # print("uptime: ", r)
#         if i == 1:
#             header = r.split(" ")
#             while "" in header:
#                 header.remove("")
#             # print(rows)
#             if header:
#                 table = PrettyTable(header)
#         if i > 1:
#             row = r.split(" ")
#             while "" in row:
#                 row.remove("")
#             # print(vals)
#             if row:
#                 table.add_row(row)
#
#     table.align = "l"
#     table.set_style(MARKDOWN)
#
#     banner("USER ON SERVER:")
#     print(table, "\n")
#
#
# def run_m(ssh_connection):
#     output = ssh_connection.run_cmd('free -hmt')
#     table = None
#     max_row = 0
#     for i, r in enumerate(output.split("\n")):
#         # print(i, r)
#
#         if i == 0:
#             header = [""] + r.split()
#             # print(header)
#             max_row = len(header)
#             if header:
#                 table = PrettyTable(header)
#                 # print(header)
#         elif i >= 1:
#             row = r.split()
#             if row:
#                 while len(row) < max_row:
#                     row.append("")
#                 # print(row)
#                 table.add_row(row)
#     table.align = "l"
#     table.set_style(MARKDOWN)
#
#     banner("MEMORY:")
#     print(table, "\n")
#
#
# def run_m_short(ssh_connection):
#     output = ssh_connection.run_cmd('free -ht')
#     for i, r in enumerate(output.split("\n")):
#         mem = r.split()
#         if i > 0 and mem:
#             txt = f"{mem[3]} / {mem[1]} ({mem[2]})"
#             print(f"{mem[0]}\t {colored(txt, 'green')} (Free/Total (Used))")
#     print("")
#
#
# def run_io(ssh_connection):
#     output = ssh_connection.run_cmd('iostat -d')
#     table = None
#
#     for i, r in enumerate(output.split("\n")):
#         # print(i, r)
#         if i == 2:
#             header = r.split()
#             # print(header)
#             if header:
#                 table = PrettyTable(header)
#         elif i >= 1:
#             row = r.split()
#             # print(row)
#             if row and "loop" not in row[0]:
#                 table.add_row(row)
#     table.align = "l"
#     # table.set_style(ORGMODE)
#     table.set_style(MARKDOWN)
#
#     banner("IO-STAT:")
#     print(table, "\n")
#
#
# def run_info(ssh_connection):
#     cpu_usage = ssh_connection.run_cmd(
#         "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'")
#     cpu_txt = f"{cpu_usage.strip()} %"
#
#     kernel_release = ssh_connection.run_cmd('uname -r')
#     kernel_name = ssh_connection.run_cmd('uname -s')
#     kernel_version = ssh_connection.run_cmd('uname -v')
#     node_name = ssh_connection.run_cmd('uname -n')
#     node_machine = ssh_connection.run_cmd('uname -m')
#     node_os = ssh_connection.run_cmd('uname -o')
#     host_name = ssh_connection.run_cmd('hostname -f')
#     host_ip = ssh_connection.run_cmd('hostname -i')
#
#     header = ['Type', 'Info']
#     table = PrettyTable(header)
#     info = ['Node name', 'Node OS', 'Mode machine', 'Kernel name', 'Kernel release', 'Kernel version']
#     info_type = [node_name, node_os, node_machine, kernel_name, kernel_release, kernel_version]
#     for k, v in zip(info, info_type):
#         # print([k, v])
#         table.add_row([k, colored(v.strip(), 'green')])
#     table.align = 'l'
#     # table.set_style(MARKDOWN)
#     banner(f"System Info: {host_name.strip()} ({host_ip.strip()})")
#     uptime = ssh_connection.run_cmd('uptime -p')
#     if uptime:
#         print(f"UPTIME: {colored(uptime, 'cyan')}")
#     print(table, "\n")
#     print("CPU usage:", colored(cpu_txt, "green"))
#
#     mem_info = ssh_connection.run_cmd('free -ht')
#     for i, r in enumerate(mem_info.split("\n")):
#         mem = r.split()
#         if i > 0 and mem:
#             txt = f"{mem[3]} / {mem[1]} ({mem[2]})"
#             print(f"{mem[0]}\t {colored(txt, 'green')} (Free/Total (Used))")
#     print("")
#
#
# def run_network(ssh_connection):
#     output = ssh_connection.run_cmd('ip a')
#     banner("Network devices")
#     # print(output)
#
#     wan_ip = ssh_connection.run_cmd("curl -A curl -s https://api.ipify.org")
#     if wan_ip:
#         print(f"WAN IP: {colored(wan_ip.strip(), 'green')}")
#
#     ip_route = ssh_connection.run_cmd("ip route | grep ^default'\s'via | head -1 | awk '{print$3}'")
#     if ip_route:
#         print(f"IP ROUTE: {colored(ip_route.strip(), 'green')}")
#
#     host_dns = ssh_connection.run_cmd("cat /etc/resolv.conf | grep -i ^nameserver | cut -d ' ' -f2")
#     if host_dns:
#         print(f"DNS: {colored(host_dns.strip(), 'green')}")
#
#     net_info = []
#     net_country = ssh_connection.run_cmd("curl -A curl -s \"http://ip-api.com/line/?fields=country\"")
#     if net_country:
#         net_info.append(net_country.strip())
#
#     net_zip = ssh_connection.run_cmd("curl -A curl -s \"http://ip-api.com/line/?fields=zip\"")
#     if net_zip:
#         net_info.append(net_zip.strip())
#
#     net_city = ssh_connection.run_cmd("curl -A curl -s \"http://ip-api.com/line/?fields=city\"")
#     if net_city:
#         net_info.append(net_city.strip())
#
#     net_isp = ssh_connection.run_cmd("curl -A curl -s \"http://ip-api.com/line/?fields=isp\"")
#     if net_isp:
#         net_info.append(net_isp.strip())
#
#     if net_info:
#         print("GEO info: ", colored(', '.join(net_info), 'green'))
#
#     pattern_mac = r"([0-9a-f]{2}(?::[0-9a-f]{2}){5})"
#     pattern_ip = r"(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?"
#     pattern_state = r"state\s(\w+)\s"
#     print("")
#     for i, r in enumerate(output.split("\n")):
#
#         dev = ''
#         ip = ''
#         mac = ''
#         try:
#             if re.search('^\d', str(r[0])):
#                 dev = f"{r.split()[0]} {r.split()[1]}"
#                 dev += f" {re.search(pattern_state, r)[1]}"
#         except Exception:
#             pass
#
#         if re.search('^\s+inet\s', r):
#             ip = [i for i in re.findall(pattern_ip, r) if '255' not in i]
#         if re.search(pattern_mac, r):
#             mac = [i for i in re.findall(pattern_mac, r) if i != 'ff:ff:ff:ff:ff:ff']
#
#         out = ''
#         if dev:
#             print(dev.strip())
#         if ip:
#             ip_f = ip
#             if "/" in ip[0]:
#                 ip_f = ip[0].split('/')[0]
#             if ip_f == ssh_connection.server:
#                 print("\tIP:", colored(ip[0].strip(), 'green'), "(connected device)")
#             else:
#                 print("\tIP:", colored(ip[0].strip(), 'green'))
#         if mac:
#             print("\tMac:", colored(mac[0].strip(), 'blue'))
#
#     print("")
#
#
# def get_server_info(ssh_connection):
#     run_info(ssh_connection)
#     run_network(ssh_connection)
#     run_m(ssh_connection)
#     run_w(ssh_connection)
#     # run_io(ssh_connection)
