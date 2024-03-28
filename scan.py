#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
from collections import OrderedDict
from flowercare import FlowerCare, FlowerCareScanner
import time
from datetime import datetime
import sys
import threading
import itertools

print(">>> Finding devices...");
print("")
# Initialize the scanner with BT interface and a 
# custom callback for newly discovered devices.
scanner = FlowerCareScanner(
    interface='hci0',  # hci0 is default, explicitly stating for demo purpose
    callback=lambda device: print(device.addr)
    # any lambda with the device as the sole argument will do
)

print(">>> Found devices:");

# Scan advertisements for 10 seconds 
# and return found device list.
devices = scanner.scan(timeout=10)
# Iterate over results and query the information 
# for each individual device.

done = False
def animate():
    for c in itertools.cycle(['.',  
                              ' .', 
                              '  .']):
        if done:
            break
        sys.stdout.write('\rWorking ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r Operation complete. ')
    sys.stdout.write('\r Data saved as \'scan_data.csv\'.')

t = threading.Thread(target=animate)
t.start()
stats = OrderedDict()
try:
    for device in devices:
        device = FlowerCare(
            mac=device.addr, # address of the device to connect to
            interface='hci0' # hci0 is default, only explicitly stating for demo purpose
        )
        stats[device.mac] = OrderedDict([
            ('MAC', device.mac),
            ('Firmware', device.firmware_version),
            ('Battery', device.battery_level)
        ])
except:
    print("Possible Error. Try again.");

# Pretty print device information
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
df = pd.DataFrame(stats.values(), index = stats.keys(),columns=['MAC', 'Firmware', 'Battery'])

print('')
print('>>> BATTERY & DEVICE INFORMATION:')
print(df)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists("scan_files"):
    os.makedirs("scan_files")
df.to_json(f'__files__/scan_files/scan_data_{timestamp}.json')
done = True
