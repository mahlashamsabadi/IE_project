import subprocess
import json 

pwd = "mahla_sh"

#stop
cmd_stop = "sudo systemctl stop nginx"
output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_stop), shell=True, capture_output=True, text=True)
print("output is ", output.stdout, "error is", output.stderr)



# start
cmd_start = "sudo systemctl start nginx"
output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)
print("output is ", output.stdout, "error is", output.stderr)



#Status
return_data = {}
cmd_status = "systemctl status nginx"
if 1==1:
    if 1==1:
        cmd_status = "systemctl status nginx"
        output = subprocess.run(cmd_status, shell=True, capture_output=True, text=True)

        return_data["stopError"] = output.stderr
        s_out = output.stdout

        if s_out != "":

            s = output.stdout
            load_s = ""

            index = s.find("Loaded: ") + 8
            while s[index]!= " " :
                 load_s += s[index]
                 index = index + 1

            return_data["Loaded"] = load_s

            active_s = ""

            index = s.find("Active: ") + 8
            while s[index]!= " " :
                 active_s += s[index]
                 index = index + 1

            return_data["Active"] = active_s

            process_s = ""

            index = s.find("Process: ") + 9
            while s[index]!= " " :
                 process_s += s[index]
                 index = index+1


            return_data["Process"] = process_s



            Pid_s = ""

            index = s.find("Main PID: ") + 10
            while s[index]!= " " :
                 Pid_s += s[index]
                 index = index + 1


            return_data["Main PID"] = Pid_s

            if active_s == "active":
                index = s.find("Tasks: ") + 7
                Tasks_s = ""

                while s[index] != " ":

                    Tasks_s += s[index]
                    index = index + 1

                return_data["Tasks"] = Tasks_s


                index = s.find("limit: ") + 7
                Task_limit = ""

                while s[index] != ")":
                    Task_limit += s[index]
                    index += 1 

                return_data["Task_limit"] = Task_limit


                Memory_s = ""
                index = s.find("Memory: ") + 8

                while s[index] != "\n":

                    Memory_s += s[index]
                    index += 1

                return_data["Memory"] = Memory_s


            cpu_s = ""

            index = s.find("CPU: ") + 5
            while s[index]!= "\n" :
                 cpu_s += s[index]
                 index = index + 1


            return_data["CPU"] = cpu_s



        return_data = json.dumps(return_data, indent = 4)


print(return_data)

