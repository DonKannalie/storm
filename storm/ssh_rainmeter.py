import os
from string import Template
import os
import re
import shutil
import pandas as pd
import numpy as np
import getpass

_user = getpass.getuser()
file = f"C:\\users\\{_user}\\.ssh\config"
target = f"C:\\Users\\{_user}\\Documents\\Rainmeter\\Skins\\ipchecker"
vpn_path = "C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe"

if not os.path.exists(target):
    os.mkdir(target)

exists_res = False


def get_hosts(config_file):
    df = pd.DataFrame(columns=["group", "var", "value"])

    first = True
    x = 0
    with open(config_file) as f:
        config = [line.rstrip('\n') for line in f]

    for cnt, line in enumerate(config):
        if re.match('Host', line) and not first:
            x += 1

        host = re.match('Host\\s(.*)', line)
        if host:
            df.loc[cnt] = [x, "host", host.group(1)]

        hostname = re.match('\s+hostname\s(.*)', line)
        if hostname:
            df.loc[cnt] = [x, "hostname", hostname.group(1)]

        user = re.match('\s+user\s(.*)', line)
        if user:
            df.loc[cnt] = [x, "user", user.group(1)]

        port = re.match('\\s+port\\s(.*)', line)
        if port:
            df.loc[cnt] = [x, "port", port.group(1)]

        first = False

    return df.pivot(index='group', columns='var', values='value')


measurer = np.vectorize(len)

df = get_hosts(file)

ip_dupl = df['hostname'].duplicated().any()

col_host_width = measurer(df['host'].values.astype(str)).max(axis=0)

info = df.sort_values('host').values
# for i in info:
#     print(i)

bg_height = (len(info) * 19) + 35

template_bat = Template("""@setlocal enableextensions enabledelayedexpansion
@echo off
set ipaddress=$ip

PING -n 1 %ipaddress% -n 1 | find /i "TTL" >nul 2>&1
IF ERRORLEVEL 1 goto :vpn
IF ERRORLEVEL 0 goto :ssh

:vpn
# start "" "${vpn_path}" --connect Dep5
echo "Hosts seems to be down"
goto :loop


:loop
timeout 2
PING -n 1 %ipaddress% -n 1 | find /i "TTL" || goto :loop
goto :ssh

:ssh
ssh ${user}@%ipaddress%

""")

head1 = f"""[Rainmeter]
Update=1000
Author=SirJ

[Background]
Meter=Image
X=10
Y=0
W=250
H={bg_height}
SolidColor=0,0,0,250

[Metadata]
Description=Displays network.
License=Creative Commons BY-NC-SA 3.0
Version=1.0.0

@include=#@#Variables.inc

"""

temp_var = """
[Variables]
; Background is based on the Background.png image that comes with the illustro skin by poiru
imageBackground=#@#BackgroundGreyTrans68h.png
;imageBackground=#@#BackgroundNavy68h.png
;imageBackground=#@#BackgroundGrey68h.png
;imageBackground=#@#BackgroundGreen68h.png
;imageBackground=#@#BackgroundRed68h.png
;imageBackground=#@#BackgroundBorderOnly68h.png

; This style is better for smaller monitors
;fontName=Trebuchet MS
;textSizeTitle=14
;textSizeData=12
;textSizeDataSmall=10
;textSizeDataTiny=8

; This style is better for larger monitors
fontName=Hack
textSizeTitle=16
textSizeData=14
textSizeDataSmall=12
textSizeDataTiny=11

colorText=255,255,255,255
colorBar=50,50,50,255
colorLightBar=150,150,150,255

; Color coding for different CPU cores
color1=25,225,25,255
color2=225,225,25,255
color3=255,150,0,255
color4=225,25,50,255
color5=0,200,255,255
color6=150,50,200,255
color7=0,0,255,255
color8=0,255,0,255

; Some extra colors
color9=100,25,150,255
color10=225,100,0,255

[styleTitle]
StringAlign=CENTER
StringStyle=BOLD
StringEffect=SHADOW
FontEffectColor=0,0,0,50
FontFace=#fontName#
FontSize=#textSizeTitle#
AntiAlias=1
ClipString=1

[styleCenterText]
StringAlign=CENTER
StringCase=NONE
StringStyle=BOLD
StringEffect=SHADOW
FontEffectColor=0,0,0,20
FontFace=#fontName#
FontSize=#textSizeData#
AntiAlias=1
ClipString=1

[styleCenterTextSmall]
StringAlign=CENTER
StringCase=NONE
FontFace=#fontName#
FontSize=#textSizeDataSmall#
AntiAlias=1
ClipString=1

[styleCenterTextTiny]
StringAlign=CENTER
StringCase=NONE
FontFace=#fontName#
FontSize=#textSizeDataTiny#
AntiAlias=1
ClipString=1

[styleDataLeft]
StringAlign=LEFT
StringCase=NONE
FontFace=#fontName#
FontSize=#textSizeData#
AntiAlias=1
ClipString=1

[styleDataLeftSmall]
StringAlign=LEFT
StringCase=NONE
FontFace=#fontName#
FontSize=#textSizeDataSmall#
AntiAlias=1
ClipString=1

[styleDataLeftTiny]
StringAlign=LEFT
StringCase=NONE
FontFace=#fontName#
FontSize=#textSizeDataTiny#
AntiAlias=1
ClipString=1

[styleDataRight]
StringAlign=RIGHT
StringCase=NONE
FontFace=#fontName#
FontSize=#textSizeData#
AntiAlias=1
ClipString=1

[styleDataRightSmall]
StringAlign=RIGHT
StringCase=NONE
FontFace=#fontName#
FontSize=#textSizeDataSmall#
AntiAlias=1
ClipString=1

[styleDataRightTiny]
StringAlign=RIGHT
StringCase=NONE
FontFace=#fontName#
FontSize=#textSizeDataTiny#
AntiAlias=1
ClipString=1

[styleSeperator]
SolidColor=255,255,255,50

[styleSeperatorHidden]
SolidColor=255,255,255,0


"""

temp_vars_bg = """
[meterTitle]
Meter=STRING
MeterStyle=styleTitle
X=140
Y=0
W=300
H=40
FontColor=#colorText#
Text="SSH Manager"
LeftMouseUpAction=!Execute ["C:\Windows\System32\control.exe" "ncpa.cpl"]
; Left-clicking this meter will open Network Connections.
ToolTipText="Network Connections"
; Hovering over this meter will display a tooltip with the text above.
"""

# temp_vars1 = Template("""
# [Measure_${hostname}]
# Measure=Plugin
# Plugin=PingPlugin
# UpdateRate=10
# DestAddress=#${ip_us}#
# Timeout=5000
# TimeoutValue=-1
# IfEqualValue=-1
# IfEqualAction=[!SetOption Meter${hostname} Text "offline"][!SetOption Meter${hostname} FontColor "255,0,0,255"][!UpdateMeter Meter${hostname}][!Redraw]
# IfAboveValue=0
# IfAboveAction=[!SetOption Meter${hostname} Text "online"][!SetOption Meter${hostname} FontColor "0,255,0,255"][!UpdateMeter Meter${hostname}][!Redraw]
# """)

temp_vars1 = Template("""
[Measure_${hostname}]
Measure=Plugin
Plugin=PingPlugin
UpdateRate=10
DestAddress=#${ip_us}#
Timeout=10000
IfBelowValue=1000
IfBelowAction=[!SetOption Meter_${hostname}Image ImageName Online.png][!UpdateMeter Meter_${hostname}Image][!Redraw]

IfAboveValue=1000
IfAboveAction=[!SetOption Meter_${hostname}Image ImageName Offline.png][!UpdateMeter Meter_${hostname}Image][!Redraw]

Substitute="30000":"-1"
""")

temp_vars2 = Template("""
[Meter_${hostname}_Label]
Meter=String
MeterStyle=styleDataLeftSmall
X=10
Y=20r
W=270
H=15
FontColor=#colorText#
Text=${hostname} ${col_host_width}> ${ip}
LeftMouseUpAction=!Execute [#${ip_us}bat#]

[Meter_${hostname}]
Meter=String
MeterStyle=styleDataRightSmall
MeasureName=Measure_${hostname}
X=280
Y=0r
W=200
H=22
FontColor=#colorText#
Text=%1

[Meter_${hostname}Image]
Meter=Image
X=0
Y=0r
W=10
H=10


""")


def main():
    t_vars1 = ""
    for hostname, ip, port, user in info:
        ip_us = f"{ip.replace('.', '_')}"
        bat_name = f"ssh_{ip_us}.bat"
        bat_file = template_bat.substitute(ip=ip, user=user, vpn_path=vpn_path)

        target_bat = os.path.join(target, 'ssh')

        if not os.path.exists(target_bat):
            os.mkdir(target_bat)

        with open(os.path.join(target_bat, bat_name), 'w') as file:
            file.write(bat_file)

        t_vars1 += f"\n{ip_us}={ip}"
        t_vars1 += f'\n{ip_us}bat="{target}\\ssh\\{bat_name}"'

    t_final = head1
    t_final += "\n[Variables]"
    # t_final += temp_vars1
    t_final += t_vars1
    t_final += '\n\n@include2=#@#Styles.inc'

    t_vars2 = ""
    for hostname, ip, port, user in info:
        ip_us = f"{ip.replace('.', '_')}"
        t_vars2 += temp_vars1.substitute(ip_us=ip_us, hostname=hostname)

    t_final += '\n\n'

    t_final += t_vars2

    t_vars3 = ""
    for hostname, ip, port, user in info:
        ip_us = f"{ip.replace('.', '_')}"
        t_vars3 += temp_vars2.substitute(
            ip_us=ip_us, ip=ip, port=port,
            hostname=hostname,
            col_host_width='-' * (int(col_host_width) - len(hostname))
        )

    t_final += temp_vars_bg
    t_final += '\n\n'
    t_final += t_vars3

    # print(t_final)

    with open(os.path.join(target, 'ssh_checker.ini'), 'w') as file:
        file.write(t_final)

    if exists_res:
        print("INFO: Ressource folder already exists")

    if ip_dupl:
        print("INFO: Found duplicate ips!!!")
        print(df[df.duplicated(['hostname'], keep=False)])


if __name__ == '__main__':
    main()
