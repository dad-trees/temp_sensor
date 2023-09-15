import asyncio

from bleak import BleakScanner, BleakClient

deviceAddresses = []

MAC_Sensor_LivingRoom   = 'A4:C1:38:6B:3A:E2'
MAC_Sensor_Bathroom     = 'A4:C1:38:3F:C3:20'

UUID_BatteryLevel       = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_SerialNumber       = '00002a25-0000-1000-8000-00805f9b34fb'
UUID_ManufacturerName   = '00002a29-0000-1000-8000-00805f9b34fb'
UUID_HardwareRevision   = '00002a27-0000-1000-8000-00805f9b34fb'
UUID_SoftwareRevision   = '00002a28-0000-1000-8000-00805f9b34fb'
UUID_FirmwareRevision   = '00002a26-0000-1000-8000-00805f9b34fb'
UUID_ManufacturerName   = '00002a29-0000-1000-8000-00805f9b34fb'
UUID_ModelNumber        = '00002a24-0000-1000-8000-00805f9b34fb'
UUID_Data               = 'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6'

async def GetSensorData(mac_address):
    retval = []
    async with BleakClient(mac_address) as client:
        sensor_data = await client.read_gatt_char(UUID_Data)
        battery_data = await client.read_gatt_char(UUID_BatteryLevel)
        battery = int.from_bytes(battery_data, byteorder='little')
        temperature = int.from_bytes(sensor_data[0:2], byteorder='little')
        humidity = int.from_bytes(sensor_data[2:3], byteorder='little')
        retval.append(temperature/100)
        retval.append(humidity/100)
        retval.append(battery/100)
    return retval

async def main():
    # living room
    sensor_data = await GetSensorData(MAC_Sensor_LivingRoom)
    print('Living Room:')
    print('  ','Temperature:', sensor_data[0])
    print('  ','Humidity:', sensor_data[1])
    print('  ','Battery:', sensor_data[2])
    print()

    sensor_data = await GetSensorData(MAC_Sensor_Bathroom)
    print('Bathroom:')
    print('  ','Temperature:', sensor_data[0])
    print('  ','Humidity:', sensor_data[1])
    print('  ','Battery:', sensor_data[2])
    print()
        

asyncio.run(main())