#!/usr/bin/env python

"""
Code to collect temperature, humidity and battery voltage from the Xiaomi LYWSD03MMC sensors
  - this will only collect sensor data at the time of execution
  - this does not collect historical data from the sensors
"""

import mysql.connector
from datetime  import datetime
import asyncio
from bleak import BleakClient
import subprocess
import os

# sensor constants
UUID_BatteryLevel   = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_Data           = 'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6'

sensor_result = []

# get data from the sensors based on the provided mac address
async def GetSensorData(mac_address):
    global sensor_result
    async with BleakClient(mac_address) as client:
        try:
            sensor_data = await client.read_gatt_char(UUID_Data)
            temperature = int.from_bytes(sensor_data[0:2], byteorder='little') / 100
            humidity = int.from_bytes(sensor_data[2:3], byteorder='little') / 100
            battery = int.from_bytes(sensor_data[3:5], byteorder='little') / 1000
            sensor_result.append(temperature)
            sensor_result.append(humidity)
            sensor_result.append(battery)
        except Exception as e:
            print(e)

# get username and password from environment variables
db_user = os.getenv('TEMP_LOGGER_USER')
db_password = os.getenv('TEMP_LOGGER_PASS')
db_server = os.getenv('DB_SERVER')
print(db_server)

# connect to database
temp_db = mysql.connector.connect(
    host = db_server,
    user = db_user,
    password = db_password,
    database = 'temperature_logs'
)

linode_db = mysql.connector.connect(
    host = '172.234.54.152',
    user = db_user,
    password = db_password,
    database = 'temperature_logs'
)

# get a db cursor for executing sql commands
temp_cursor = temp_db.cursor()
linode_cursor = linode_db.cursor()

# get list of sensors
ts = datetime.now()
recordTimestamp = ts.strftime('%Y-%m-%d %H:%M:%S')

print(recordTimestamp, 'Getting list of sensors...')
sql = 'select mac_address from sensors'
temp_cursor.execute(sql)
sql_result = temp_cursor.fetchall()

ts = datetime.now()
recordTimestamp = ts.strftime('%Y-%m-%d %H:%M:%S')
print(recordTimestamp, 'Found {} sensors.'.format(len(sql_result)))

# for address in sql_result:
#     subprocess.call(['bluetoothctl', 'disconnect', address[0]])

# collect data from sensors and save to database
for address in sql_result:
    mac = address[0]
    ts = datetime.now()
    recordTimestamp = ts.strftime('%Y-%m-%d %H:%M:%S')
    print(recordTimestamp, 'Retrieving sensor data from {}'.format(mac))
    
    # get data from sensor
    try:
        sensor_result = []
        asyncio.run(GetSensorData(mac))
    
        sql = "INSERT IGNORE INTO data_logs (mac_address, log_timestamp, temperature, humidity, battery) VALUES ('{}', '{}', {}, {}, {})".format(mac, recordTimestamp, sensor_result[0], sensor_result[1], sensor_result[2])
        temp_cursor.execute(sql)
        temp_db.commit()
        linode_cursor.execute(sql)
        linode_db.commit()

        ts = datetime.now()
        recordTimestamp = ts.strftime('%Y-%m-%d %H:%M:%S')

        print(recordTimestamp, 'Uploaded sensor data to database.')

    except Exception as e:
        print(recordTimestamp,'Error: {}'.format(e))

# disconnect from database
temp_db.disconnect()
linode_db.disconnect()

# disconnect from bluetooth devices
for address in sql_result:
    subprocess.call(['bluetoothctl', 'disconnect', address[0]])



