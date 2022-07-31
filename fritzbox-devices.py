import sys
import json
import time
import datetime
import itertools
import os
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzwlan import FritzWLAN
from fritzconnection.lib.fritzhosts import FritzHosts
from fritzconnection.core.exceptions import FritzServiceError

from dotenv import load_dotenv,dotenv_values
from influxSubmitter import toInflux
load_dotenv()

wlanServices = {
    1:"2.4ghz",
    2:"5ghz",
    3:"Guest",
}

def getConnectedDevices(wifiDevices = False):
    fh = FritzHosts(address=os.getenv('FRITZBOX_HOST'), user=os.getenv('FRITZBOX_USER'), password=os.getenv('FRITZBOX_PASSWORD'))
    hosts = fh.get_hosts_info()
    for index, host in enumerate(hosts, start=1):
        status = True if host['status'] else  False
        ip = host['ip'] if host['ip'] else '-'
        mac = host['mac'] if host['mac'] else '-'
        macWoDots = ''.join(mac.split(':'))
        hn = host['name']
        inf = host['interface_type'] if host['interface_type'] else '-'
        inf = 'WiFi' if inf == '802.11' else 'Ethernet' if inf == 'Ethernet' else 'unknown'
        wifiDevice = ''
        
        toInflux('devices', f'ip="{ip}",hostname="{hn}",interface="{inf}",active={status}', f'mac={mac},hostname={hn},ip={ip},interface={inf}')
        
        if wifiDevices != False and macWoDots != '-' and inf == 'WiFi':
            if macWoDots in wifiDevices:
                wifiDeviceData = wifiDevices[macWoDots]
                signal = wifiDeviceData['signal']
                wlan = wifiDeviceData['wlan']
                speed = wifiDeviceData['speed']
                wifiDevice = f'{wlan:<5} {signal:<16} {speed:<10}'
                toInflux('devices', f'signal={signal}i,wlan="{wlan}",speed={speed}i', f'mac={mac},hostname={hn},ip={ip},interface={inf}')
            
        # print(f'{index:>3}: {ip:<16} {hn:<40} {mac:<17} {inf:<10} {status:<10} {wifiDevice}')
        

def getWifiDevices(): 
    devices = {}
    for index, name in wlanServices.items():
        fw_local = FritzWLAN(address=os.getenv('FRITZBOX_HOST'), user=os.getenv('FRITZBOX_USER'), password=os.getenv('FRITZBOX_PASSWORD'), service=index)
        hosts = fw_local.get_hosts_info()
        for i, host in enumerate(hosts, start=1):
            detail = host
            detail['wlan'] = name
            mac = detail['mac']
            macWoDots = ''.join(mac.split(':'))
            devices[macWoDots] = detail
            # print(f'{i:>3}: {name:<6} {mac:<17} {macWoDots:<16}')
    return devices

if __name__ == '__main__':
    i = 0
    while True:
        getConnectedDevices(getWifiDevices())
        i = i+10
        if i > 60:
            break