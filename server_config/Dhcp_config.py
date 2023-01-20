import os
import subprocess
import json

return_data = {}

out = subprocess.run('sudo /etc/init.d/dhcp start', shell=True, capture_output=True, text=True)