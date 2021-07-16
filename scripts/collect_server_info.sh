#!/bin/bash

uptime=$(uptime -p)
cpu_threads=$(lscpu | grep "Thread(s) per core:" | awk -F":" '{print $2}' | awk '{$1=$1;print}')
cpu_load=$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}')
cpu_cores=$(lscpu | grep "Core(s) per socket:" | awk -F":" '{print $2}' | awk '{$1=$1;print}')
cpu_sockets=$(lscpu | grep "Socket(s):" | awk -F":" '{print $2}' | awk '{$1=$1;print}')
cpu_name=$(lscpu | grep "Model name:" | awk -F":" '{print $2}' | awk '{$1=$1;print}')
cpu_mhz_=$(lscpu | grep "CPU MHz:" | awk -F":" '{print $2}' | awk '{$1=$1;print}')
cpu_mhz=$(printf "%.*f\n" "0" "$cpu_mhz_")
cpu_max_=$(lscpu | grep "CPU max MHz:" | awk -F":" '{print $2}' | awk '{$1=$1;print}')
cpu_max=$(printf "%.*f\n" "0" "$cpu_max_")
cpu_virt=$(lscpu | grep "Virtualization" | awk -F":" '{print $2}' | awk '{$1=$1;print}')
mem=$(free -h)
mem_total=$(echo "$mem" | grep Mem: | awk '{ print $2 }')
mem_free=$(echo "$mem" | grep Mem: | awk '{ print $4 }')
mem_used=$(echo "$mem" | grep Mem: | awk '{ print $3 }')
mem_avail=$(echo "$mem" | grep Mem: | awk '{ print $2 }')
swap_total=$(echo "$mem" | grep Swap: | awk '{ print $2 }')
swap_free=$(echo "$mem" | grep Swap: | awk '{ print $4 }')
swap_used=$(echo "$mem" | grep Swap: | awk '{ print $3 }')
swap_avail=$(echo "$mem" | grep Swap: | awk '{ print $2 }')
kernel_release=$(uname -r)
kernel_name=$(uname -s)
kernel_version=$(uname -v)
node_name=$(uname -n)
node_machine=$(uname -m)
node_os=$(cat /etc/*release | grep PRETTY_NAME | awk -F"=" '{print $2}')
host_name=$(hostname -f)
host_ip=$(hostname -i)
wan_ip=$(curl -A curl -s https://api.ipify.org)
ip_dhcp=$(ip r | grep default | grep dhcp -oq && echo "true" || echo "false")
ip_route=$(ip route | grep ^default'\s'via | head -1 | awk '{print$3}')
host_dns=$(cat /etc/resolv.conf | grep -i ^nameserver | cut -d ' ' -f2)
net_country=$(curl -A curl -s "http://ip-api.com/line/?fields=country")
net_zip=$(curl -A curl -s "http://ip-api.com/line/?fields=zip")
net_city=$(curl -A curl -s "http://ip-api.com/line/?fields=city")
net_isp=$(curl -A curl -s "http://ip-api.com/line/?fields=isp")
package_upgrade=$(apt list --upgradable | wc -l)

echo "uptime=$uptime"
echo "node_name=$node_name"
echo "node_os=$node_os"
echo "node_machine=$node_machine"
echo "kernel_release=$kernel_release"
echo "kernel_name=$kernel_name"
echo "kernel_version=$kernel_version"
echo "host_name=$host_name"
echo "cpu_name=$cpu_name"
echo "cpu_load=$cpu_load %"
echo "cpu_speed=$cpu_mhz Mhz ($cpu_max Mhz)"
echo "cpu_info=cores: $cpu_cores threads: $cpu_threads sockets: $cpu_sockets"
echo "cpu_virt=$cpu_virt"
echo "ram=$mem_total|$mem_free|$mem_used|$mem_avail (T|F|U|A)"
echo "smap=$swap_total|$swap_free|$swap_used|$swap_avail (T|F|U|A)"
echo "host_ip=$host_ip"
echo "wan_ip=$wan_ip"
echo "ip_route=$ip_route"
echo "host_dns=$host_dns"
echo "dhcp=$ip_dhcp"
echo "net_country=$net_country"
echo "net_zip=$net_zip"
echo "net_city=$net_city"
echo "net_isp=$net_isp"
echo "package_upgrade=$package_upgrade"
