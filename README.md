# Temperature Sensor
This is a simple code that collects data from the temperature and humidity sensor LYWSD03MMC.  The code collects the current temperature, humidity and battery voltage from the sensor and save those pieces of information to a database.   

## Requirements
mysql.connector  
asyncio  
bleak  
subprocess  
io  

## Files
temp_logger.py - the main code file  
data_logs.sql - sql command to create the table structure needed for storing the collected data  
