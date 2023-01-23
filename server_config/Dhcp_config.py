import os
import subprocess
import json

return_data = {}
pwd = "mahla_sh"

#Start Dhcp
cmd_start = "sudo service isc-dhcp-server start"
output_start = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)
print("output is", output_start.stdout, "error is",output_start.stderr)


#Stop Dhcp
cmd_stop = "sudo service isc-dhcp-server stop"
output_stop = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_stop), shell=True, capture_output=True, text=True)
print("output is", output_stop.stdout, "error is",output_stop.stderr)


#Status
output_status = subprocess.run('sudo service isc-dhcp-server status', shell=True, capture_output=True, text=True)
print("output is", output_status.stdout, "error is",output_status.stderr)


#/etc/dhcp/dhcpd.conf
#Change IP Range
