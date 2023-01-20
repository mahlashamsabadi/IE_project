import os
import subprocess
import json

return_data = {}
pwd = "fatemeh"

#Start Dhcp
cmd_start = "sudo /etc/init.d/dhcp start"
output_start = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)
print("output is", output_start.stdout, "error is",output_start.stderr)


#Stop Dhcp
cmd_stop = "sudo /etc/init.d/dhcp stop"
output_stop = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_stop), shell=True, capture_output=True, text=True)
print("output is", output_stop.stdout, "error is",output_stop.stderr)


#Status
output_status = subprocess.run('systemctl status dhcp', shell=True, capture_output=True, text=True)
print("output is", output_status.stdout, "error is",output_status.stderr)


