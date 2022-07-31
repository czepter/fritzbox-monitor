import re
import subprocess
from datetime import datetime

from dotenv import load_dotenv,dotenv_values
from influxSubmitter import toInflux
load_dotenv()

response = subprocess.Popen('speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
jitter = re.search('\((.*?)\s.+jitter\)\s', response, re.MULTILINE)

error = re.search('\((.*?)\s.+Error\)\s', response, re.MULTILINE)

ping = 0
download = 0
upload = 0
jitter = 0
result_error = 'false'

if error is None:
    ping = ping.group(1)
    download = download.group(1)
    upload = upload.group(1)
    jitter = jitter.group(1)
    
else:
    result_error = 'true'

toInflux('speedtest', f'download={download},upload={upload},ping={ping},jitter={jitter},error={result_error}')