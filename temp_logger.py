#!/usr/bin/env python

import mysql.connector
from datetime  import datetime
import asyncio
from bleak import BleakScanner, BleakClient

# sensor constants
UUID_BatteryLevel   = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_Data           = 'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6'

sensors = ['A4:C1:38:6B:3A:E2', 'A4:C1:38:3F:C3:20']

sensor_result = []

async def GetSensorData(mac_address):
    global sensor_result
    client = BleakClient(mac_address)
    try:
        await client.connect()
        sensor_data = await client.read_gatt_char(UUID_Data)
        battery_data = await client.read_gatt_char(UUID_BatteryLevel)
        battery = int.from_bytes(battery_data, byteorder='little') / 100
        temperature = int.from_bytes(sensor_data[0:2], byteorder='little') / 100
        humidity = int.from_bytes(sensor_data[2:3], byteorder='little') / 100
        sensor_result.append(temperature)
        sensor_result.append(humidity)
        sensor_result.append(battery)
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()



# connect to database
temp_db = mysql.connector.connect(
    host = '192.168.100.4',
    user = 'temp_logger',
    password = 'temp_admin',
    database = 'temp_logs'
)

temp_cursor = temp_db.cursor()

# get list of sensors
print('Getting list of sensors...')
sql = 'select mac_address from sensors'
temp_cursor.execute(sql)
sql_result = temp_cursor.fetchall()
print('Found {} sensors.'.format(len(sql_result)))

for address in sql_result:
    mac = address[0]
    print('Retrieving sensor data from {}'.format(mac))
    
    ts = datetime.now()
    recordTimestamp = ts.strftime('%Y-%m-%d %H:%M:%S')

    # get data from sensor
    sensor_result = []
    asyncio.run(GetSensorData(mac))

    sql = "INSERT IGNORE INTO data_logs (mac_address, log_timestamp, temperature, humidity, battery) VALUES ('{}', '{}', {}, {}, {})".format(mac, recordTimestamp, sensor_result[0], sensor_result[1], sensor_result[2])
    temp_cursor.execute(sql)
    temp_db.commit()
    print('Uploaded sensor data to database.')
    print()


# disconnect from database
temp_db.disconnect()

