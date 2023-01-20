import os
import subprocess
import json

json_data = {}

out = subprocess.run('sudo systemctl status postfix', shell=True, capture_output=True, text=True)
#out2 = subprocess.run('/etc/init.d/postfix start', shell=True, capture_output=True, text=True)

#out3 = subprocess.run('/etc/init.d/postfix stop', shell=True, capture_output=True, text=True)
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