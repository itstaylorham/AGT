from pickle import TRUE
import pandas as pd
from flowercare import FlowerCare
import time
import sys
import threading
import itertools

while 1:
    print("FIND...")
    usrinpt = input("Please enter device mac:")

    def pass_id(device_id):
        if usrinpt == TRUE:
            usrinpt == device_id
        return device_id
            
    # Initialize FlowerCare device
    device = FlowerCare(
        mac='c4:7c:8d:6d:' + pass_id(usrinpt), # device address
        interface='hci0' # hci0 is default, explicitly static for demo purpose
    )
    print("");
    print("Device Details")
    df_systats = pd.DataFrame
    print('Address: {}'.format(device.mac))
    print('Firmware: {}'.format(device.firmware_version))
    print('Battery: {}%'.format(device.battery_level))
    print("");
    print("Sensor Readings")
    real_time_data = device.real_time_data
    print('Temperature: {}°C'.format(real_time_data.temperature))
    print('Moisture: {}%'.format(real_time_data.moisture))
    print('Light: {} lux'.format(real_time_data.light))
    print('Conductivity: {} µS/cm'.format(real_time_data.conductivity))
    print("")
    ## Errors
    try:
        y = eval(usrinpt)
        if y: print(y)
    except:
        try:
            exec(usrinpt)
        except Exception as e:
            print("ERROR", e);


# Display historical sensor readings
# print('\nHistorical data\n----')
# historical_data = device.historical_data
# for entry in historical_data:
#     print('Timestamp: {}'.format(entry.timestamp))
#     print('Temperature: {}°C'.format(entry.temperature))
#     print('Moisture: {}%'.format(entry.moisture))
#     print('Light: {} lux'.format(entry.light))
#     print('Conductivity: {} µS/cm\n'.format(entry.conductivity))
