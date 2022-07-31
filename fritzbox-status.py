import sys
import json
import time
import datetime
import itertools
import os

from fritzconnection import FritzConnection
from fritzconnection.lib.fritzwlan import FritzWLAN
from fritzconnection.lib.fritzhosts import FritzHosts
from fritzconnection.lib.fritzstatus import FritzStatus
from fritzconnection.core.exceptions import FritzServiceError

from influxSubmitter import toInflux,load_dotenv
load_dotenv()


fs = FritzStatus(address=os.getenv('FRITZBOX_HOST'), user=os.getenv('FRITZBOX_USER'), password=os.getenv('FRITZBOX_PASSWORD'))
fc = FritzConnection(address=os.getenv('FRITZBOX_HOST'), user=os.getenv('FRITZBOX_USER'), password=os.getenv('FRITZBOX_PASSWORD'))

def getStatus():
    device_uptime = fs.device_uptime
    version = fc.system_version
    toInflux('status', f'device_uptime={device_uptime}i,version={version}')

def getThroughput():
    transmission_rate_up, transmission_rate_down = fs.transmission_rate
    toInflux('throughput', f'bytes_rate_up={transmission_rate_up}i,bytes_rate_down={transmission_rate_down}i')
    mbits_rate_up = transmission_rate_up / 1000000 * 8
    mbits_rate_down = transmission_rate_down / 1000000 * 8
    toInflux('throughput', f'mbits_rate_up={mbits_rate_up},mbits_rate_down={mbits_rate_down}')

    # attenuation_up, attenuation_down = fs.attenuation
    # toInflux('throughput', f'attenuation_up={attenuation_up}i,attenuation_down={attenuation_down}i')

    bytes_received = fs.bytes_received
    bytes_sent = fs.bytes_sent
    toInflux('throughput', f'bytes_received={bytes_received}i,bytes_sent={bytes_sent}i')
    mbytes_received = fs.bytes_received/ 1000000
    mbytes_sent = fs.bytes_sent/ 1000000
    toInflux('throughput', f'mbytes_received={mbytes_received},mbytes_sent={mbytes_sent}')

    gbytes_received = fs.bytes_received/ 1000000 / 1000
    gbytes_sent = fs.bytes_sent/ 1000000 / 1000
    toInflux('throughput', f'gbytes_received={gbytes_received},gbytes_sent={gbytes_sent}')

def getConnection():
    connection_uptime = fs.connection_uptime
    is_connected = fs.is_connected
    is_linked = fs.is_linked
    toInflux('connection', f'connection_uptime={connection_uptime}i,is_connected={is_connected},is_linked={is_linked}')

    external_ip = fs.external_ip
    external_ipv6 = fs.external_ipv6
    toInflux('connection', f'external_ipv6="{external_ipv6}",external_ip="{external_ip}"')

    max_bit_rate_up, max_bit_rate_down = fs.max_bit_rate
    toInflux('connection', f'max_bit_rate_up={max_bit_rate_up}i,max_bit_rate_down={max_bit_rate_down}i')

    max_linked_bit_rate_up, max_linked_bit_rate_down = fs.max_linked_bit_rate
    toInflux('connection', f'max_linked_bit_rate_up={max_linked_bit_rate_up}i,max_linked_bit_rate_down={max_linked_bit_rate_down}i')
    
    noise_margin_up, noise_margin_down = fs.noise_margin
    toInflux('connection', f'noise_margin_up={noise_margin_up}i,noise_margin_down={noise_margin_down}i')

if __name__ == '__main__':
    getStatus()
    getConnection()
    
    i = 0
    while True:
        getThroughput()
        time.sleep(5)
        i = i+5
        if i > 60:
            break

