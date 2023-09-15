#!/usr/bin/env python

import asyncio
from bleak import BleakClient

sensor = 'A4:C1:38:3F:C3:20'

# sensor constants
UUID_BatteryLevel   = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_Data           = 'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6'

async def GetServices():
    async with BleakClient(sensor) as client:
        battery = await client.read_gatt_char(UUID_BatteryLevel)
        data = await client.read_gatt_char(UUID_Data)
        battery_level = int.from_bytes(battery, byteorder='little')
        temperature = int.from_bytes(data[0:2], byteorder='little')
        humidity = int.from_bytes(data[2:3], byteorder='little')
        battery_voltage = int.from_bytes(data[3:5], byteorder='little')
        print(temperature)
        print(humidity)
        print(battery_level)
        print(battery_voltage)


asyncio.run(GetServices())