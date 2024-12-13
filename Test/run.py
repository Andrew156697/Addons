import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# config 
bucket="storage"
token = "5VXStBHdRgn-NxSy_cxzqzSU0EaAR1OSzLESuKPjV3_IV85EelzvO2RMU_LeJOgTy0iEsxABRraKLxdBnIbv-w=="
org = "chtlab"
url = "http://192.168.1.29:8086"

client = InfluxDBClient(
    url=url, 
    token=token, 
    org=org
)
write_api = client.write_api(write_options=SYNCHRONOUS)
data = Point()
write_api.write(bucket=bucket,org=org,record=data)

