import os
import subprocess
import json

json_data = {}

out = subprocess.run('sudo systemctl status postfix', shell=True, capture_output=True, text=True)


pwd = "fatemeh" # write your password here!
cmd = "sudo /etc/init.d/postfix start"

out2 = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd), shell=True, capture_output=True, text=True)
print("the output2 is",out2.stdout, out2.stderr)

cmd2 = 'sudo /etc/init.d/postfix stop'
out3 = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd2), shell=True, capture_output=True, text=True)
print("the output3 is",out3.stdout)


s = out.stdout
load_s = ""

index = s.find("Loaded: ") + 8
while s[index]!= " " :
     load_s += s[index]
     index = index+1

json_data["Loaded"] = load_s

active_s = ""

index = s.find("Active: ") + 8
while s[index]!= " " :
     active_s += s[index]
     index = index+1

json_data["Active"] = active_s

process_s = ""

index = s.find("Process: ") + 9
while s[index]!= " " :
     process_s += s[index]
     index = index+1


json_data["Process"] = process_s



PID_s = ""

index = s.find("Main PID: ") + 10
while s[index]!= " " :
     PID_s += s[index]
     index = index+1


json_data["Main PID: "] =PID_s

CPU_s = ""

index = s.find("CPU: ") + 5
while s[index]!= "\n" :
     CPU_s += s[index]
     index = index+1


json_data["CPU: "] =CPU_s

json_data = json.dumps(json_data, indent = 4)
print(json_data, type(json_data))