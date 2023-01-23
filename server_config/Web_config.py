import subprocess


pwd = "mahla_sh"

#Start nginx

cmd_start = "sudo systemctl stop nginx"
output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)
print("output is ", output.stdout, "error is", output.stderr)

#Stop nginx
cmd_start = "sudo systemctl start nginx"
output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)
print("output is ", output.stdout, "error is", output.stderr)

#Status
output_status = subprocess.run('service isc-dhcp-server status', shell=True, capture_output=True, text=True)
print("output is", output_status.stdout, "error is",output_status.stderr)