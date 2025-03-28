#!/bin/bash
pip3 install bluepy;
cd /home/jerremy/Documents/GitHub/AGT/env/lib/python3.13/site-packages/bluepy/;
chmod +x bluepy-helper;
sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper;
getcap bluepy-helper;