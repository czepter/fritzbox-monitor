from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv,dotenv_values
import os

load_dotenv()

client = InfluxDBClient(url=os.getenv('INFLUX_HOST'), token=os.getenv('INFLUX_TOKEN'))
write_api = client.write_api(write_options=SYNCHRONOUS)

def toInflux(measurement, values, tags=''):
    data = measurement

    if tags != '':
        data = data + ',' + tags

    data = data+" "+values

    if os.getenv('INFLUX_SUBMIT') == 'True':
        write_api.write(os.getenv('INFLUX_BUCKET'), os.getenv('INFLUX_ORG'), data)
        #print(f'write done: {data}')
    else:
        valuesList = values.split(",")
        valuesList = "\n\t".join(valuesList)
        print("measurement: {measurement}".format(measurement=measurement))
        print("tags: {tags}".format(tags=tags))
        print("values:\n\t{values}".format(values=valuesList))
        print("\n")