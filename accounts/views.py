from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from rest_framework_tracking.mixins import LoggingMixin
from permissions import *
from rest_framework import generics
import sqlite3
from sqlite3 import Error
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from subprocess import Popen, PIPE
import subprocess
import json
import fileinput
import re
import ast

class Register(LoggingMixin ,APIView):
    def post(self, request):
        serialized_data = UserRegisterSerializer(data=request.data)
        data = {}
        if serialized_data.is_valid():
            account = serialized_data.save()
            data['username'] = account.username
            data['email'] = account.email
            data['type'] = account.type
            refresh = RefreshToken.for_user(account)
            data['access'] = str(refresh.access_token)
            return Response(data)
        return Response(serialized_data.errors)

class CustomTokenObtainPairView(LoggingMixin, TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer

class AddUserMail(LoggingMixin ,APIView):

    def post(self, request):


        return_data = {}
        username = request.data["username"]
        password = request.data["password"]

        if username = "" or password = "": 
            
            return_data["addUserOutput"] = ""
            return_data["addUserError"] = "invalid value for username or password."
            return Response(return_data,status=400)

        if username[0].isdigit():

            return_data["addUserOutput"] = ""
            return_data["addUserError"] = "The username cannot start with a number."
            return Response(return_data,status=400)

        cmd1 = 'sudo adduser --gecos "" ' + username
        output1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
        return_data["addUserOutput"] = output1.stdout
        return_data["addUserError"] = output1.stderr
        if return_data["addUserError"].find("already exists.") != -1:
            return Response(return_data, status = 400)
        if return_data["addUserError"] != "":
            return Response(return_data, status=500)
        cmd2 = "sudo passwd -d "+ username
        subprocess.run(cmd2, shell=True, capture_output=True, text=True)
        proc=Popen(['sudo', 'passwd', 'soha4'],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        proc.stdin.write(password+"\n".encode())
        proc.stdin.write(password.encode())
        proc.stdin.flush()
        stdout,stderr = proc.communicate()
        return_data["addPassOutput"] = stdout
        return_data["addPassError"] = stderr

        if return_data["addPassError"] != "":
            return Response(return_data, status=500)
        
        return Response(return_data, status=200)


class DhcpConfigStart(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser | IsDhcpManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        #change password
        cmd_start = "sudo service isc-dhcp-server start"
        output = subprocess.run(cmd_start, shell=True, capture_output=True, text=True)

        return_data["startError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)

        #IDSC
        cmd_mail = "mutt -s 'DHCP server Started'  admin@UIIE.LOC <  /var/www/Mails/Mail_dhcp_start.txt"
        output = subprocess.run(cmd_mail, shell=True, capture_output=True, text=True)

        return Response(dict_data)

class DhcpConfigStop(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsDhcpManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}

        cmd_stop = "sudo service isc-dhcp-server stop"
        output = subprocess.run(cmd_stop, shell=True, capture_output=True, text=True)

        return_data["stopError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)

        #IDSC
        cmd_mail = "mutt -s 'DHCP server Stopped'  admin@UIIE.LOC <  /var/www/Mails/Mail_dhcp_stop.txt"
        output = subprocess.run(cmd_mail, shell=True, capture_output=True, text=True)

        return Response(dict_data)



class DhcpConfigStatus(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser |IsDhcpManager,]

    def get(self, request):

        return_data ={} 

        cmd_status = "sudo service isc-dhcp-server status"
        output = subprocess.run(cmd_status, shell=True, capture_output=True, text=True)


        return_data["statusError"] = output.stderr

            
        if  output.stdout != "":

            s = output.stdout
            load_s = ""

            index = s.find("Loaded: ") + 8
            while s[index]!= " " :
                load_s += s[index]
                index = index+1

            return_data["Loaded"] = load_s

            active_s = ""

            index = s.find("Active: ") + 8

            while s[index]!= " " :
                active_s += s[index]
                index = index+1

            return_data["Active"] = active_s

            process_s = ""

            index = s.find("Process: ") + 9

            while s[index]!= " " :

                process_s += s[index]
                index = index+1


            return_data["Process"] = process_s



            Pid_s = "" #؟؟

            index = s.find("Main PID: ") + 10
            while s[index]!= " " :
                Pid_s += s[index]
                index = index+1


            return_data["Main PID"] =Pid_s

        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)
        return Response(dict_data)



# ?
class DhcpConfigChangeIpRange(LoggingMixin , generics.GenericAPIView): 
    permission_classes = [IsAdminUser |IsDhcpManager,]

    def post(self, request):
        self.check_object_permissions(request , request.user)
        #retrun error if stat_ip and end_ip are not correct
        # is it correct
        int_start = int(request.data.startip)
        int_end = int(request.data.endip)
        return_data = {}
        if int_start < 1 or int_start > int_end or int_end > 255:
            return_data["change_range"] = "Unacceptable value for IPs"
            return_data = json.dumps(return_data, indent = 4)
            return Response(return_data, status=400)

        new_start_ip = "192.168.10." + request.data.startip
        new_end_ip = "192.168.10."+ request.data.endip

        word = 'range'
        word = word
        strt_ip = ""
        end_ip = ""

        #retrun Error if we could not open file
        with open('/etc/dhcp/dhcpd.conf','r+') as fp:

        
            lines = fp.readlines()
            filedata = fp.read()

            for line in lines:

                s = str(line)
                if line.find(word) != -1:

                    index = s.find("range ") + 6
                    
                    while s[index]!= " " :
                        strt_ip += s[index]
                        index = index+1
                    index += 1
                    while s[index]!= ";" :
                        end_ip += s[index]
                        index = index+1
                    if strt_ip != "" and end_ip !="":
                        break

            if strt_ip == "" or end_ip =="":
                return_data["change_range"] = "Can not found the range definition in config file!"
                return_data = json.dumps(return_data, indent = 4)
                return Response(return_data, status=500)
            

        file = open('/etc/dhcp/dhcpd.conf','r+')
        replaced_content = ""
        for line in file:
            new_line = line 

            if line.find("range "+strt_ip+" "+ end_ip+";") != -1:
                new_line = "  range "+ new_start_ip + " " + new_end_ip + ";\n"

            replaced_content = replaced_content + new_line
        file.close()
        write_file = open('/etc/dhcp/dhcpd.conf', "w")

        write_file.write(replaced_content)
        write_file.close()
        return_data["change_range"] = "The ip Range successfully changed."
        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)

        #IDSC
        cmd_mail = "mutt -s 'IP range changed'  admin@UIIE.LOC <  /var/www/Mails/Mail_dhcp_Change_Ip_range.txt"
        output = subprocess.run(cmd_mail, shell=True, capture_output=True, text=True)

        #Restart DHCP
        cmd_restart = "sudo service isc-dhcp-server restart"
        output = subprocess.run(cmd_restart, shell=True, capture_output=True, text=True)

        return Response(dict_data, status = 200)


class MailConfigStart(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser |IsMailManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        #it should change to server password!

        cmd = "sudo /etc/init.d/postfix start"

        output = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        return_data ={}
        return_data["startOutput"] = output.stdout
        return_data["startError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)


        #IDSC
        cmd_mail = "mutt -s 'Mail server Started'  admin@UIIE.LOC <  /var/www/Mails/Mail_Mail_start.txt"
        output = subprocess.run(cmd_mail, shell=True, capture_output=True, text=True)
        return Response(dict_data)

class MailConfigStop(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser |IsMailManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        cmd = "sudo /etc/init.d/postfix stop"

        output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return_data ={} 
        return_data["stopOutput"] = output.stdout
        return_data["stopError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)

        #IDSC
        cmd_mail = "mutt -s 'Mail server Stopped'  admin@UIIE.LOC <  /var/www/Mails/Mail_Mail_stop.txt"
        output = subprocess.run(cmd_mail, shell=True, capture_output=True, text=True)
        return Response(dict_data)


class MailConfigStatus(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser |IsMailManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data ={} 

        output = subprocess.run('systemctl status postfix', shell=True, capture_output=True, text=True)

        return_data["statusError"] = output.stderr

        s_out = output.stdout
        
        if s_out != "":

            s = output.stdout
            load_s = ""

            index = s.find("Loaded: ") + 8
            while s[index]!= " " :
                 load_s += s[index]
                 index = index+1

            return_data["Loaded"] = load_s

            active_s = ""

            index = s.find("Active: ") + 8
            while s[index]!= " " :
                 active_s += s[index]
                 index = index+1

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
                 index = index+1


            return_data["Main PID"] =Pid_s

            cpu_s = ""

            index = s.find("CPU: ") + 5
            while s[index]!= "\n" :
                 cpu_s += s[index]
                 index = index+1


            return_data["CPU"] =cpu_s

        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)
        return Response(dict_data)

class WebServerConfigStart(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser |IsWebManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}

        cmd_start = "sudo systemctl start nginx"
        output = subprocess.run(cmd_start, shell=True, capture_output=True, text=True)

        return_data["startError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)
        #IDSC
        cmd_mail = "mutt -s 'Web server Started'  admin@UIIE.LOC < /var/www/Mails/Mail_Web_start.txt"
        output = subprocess.run(cmd_mail, shell=True, capture_output=True, text=True)
        return Response(dict_data)

class WebServerConfigStop(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser |IsWebManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        #change password
    
        cmd_stop = "sudo systemctl stop nginx"
        output = subprocess.run(cmd_stop, shell=True, capture_output=True, text=True)

        return_data["stopError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)

        #IDSC
        cmd_mail = "mutt -s 'Web server Stopped'  admin@UIIE.LOC <  /var/www/Mails/Mail_Web_stop.txt"
        output = subprocess.run(cmd_mail, shell=True, capture_output=True, text=True)
        return Response(dict_data)


class WebServerConfigStatus(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser |IsWebManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        cmd_status = "systemctl status nginx"
        output = subprocess.run(cmd_status, shell=True, capture_output=True, text=True)

        return_data["statusError"] = output.stderr
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
        dict_data = ast.literal_eval(return_data)

class WebServerConfigGetHomeDir(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser | IsWebManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        current_Dir = ""
        word = 'root'

        with open('/etc/nginx/sites-available/Internet-engineering-proj.conf','r+') as fp:

            # read all lines in a list
            lines = fp.readlines()
            filedata = fp.read()
            
            for line in lines:
                # check if string present on a current line
                s = str(line)
                if line.find(word) != -1:

                    index = s.find("root ") + 5
                    
                    while s[index]!= ";" :
                        current_Dir += s[index]
                        index = index+1
                    break

        return_data["HomeDir"] = current_Dir
        return_data = json.dumps(return_data, indent = 4)
        dict_data = ast.literal_eval(return_data)

        return Response(dict_data)

class WebServerConfigChangeHomeDir(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsAdminUser |IsWebManager,]

    def post(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        new_dir = request.data['newDirectory']
        current_Dir = ""
        word = 'root'

        with open('/etc/nginx/sites-available/Internet-engineering-proj.conf','r+') as fp:

            # read all lines in a list
            lines = fp.readlines()
            filedata = fp.read()
            for line in lines:
                # check if string present on a current line
                s = str(line)
                if line.find(word) != -1:

                    index = s.find("root ") + 5
                    
                    while s[index]!= ";" :
                        current_Dir += s[index]
                        index = index+1
                    break

        
        Dirs = new_dir.split("/")
        index = 0
        first_cd = "/var/www"
        namoshtarak = ""
        while current_Dir.find(Dirs[index]) != -1:
            first_cd = first_cd + "/" + Dirs[index]
            index += 1
        first_cd += "/"
        new_edited_dir = new_dir
        if index != 0:
            namoshtarak = Dirs[index]
            new_edited_dir = ""
            while index < len(Dirs):
                new_edited_dir = new_edited_dir + Dirs[index] +"/"
                index += 1  

            output_cd1 = subprocess.run("cd " + first_cd, shell=True, capture_output=True, text=True)
            output_mkdir = subprocess.run('mkdir -p '+ new_edited_dir, shell=True, capture_output=True, text=True)
            if index == 0:
                output_cp = subprocess.run("sudo cp -r "+ current_Dir+"/!" + " " +"./"+ new_dir, shell=True, capture_output=True, text=True)
            else:
                output_cp = subprocess.run("sudo cp -r "+ current_Dir +"/!("+namoshtarak+")" + " " +"./"+ new_edited_dir, shell=True, capture_output=True, text=True)
            if index == 0:
                output_rm = subprocess.run("sudo rm -rf  "+ current_Dir+"/*" , shell=True, capture_output=True, text=True)
            else:
                output_rm = subprocess.run("sudo rm -rf -v "+ current_Dir+"/!("+namoshtarak+")" , shell=True, capture_output=True, text=True)

            output_cd2 = subprocess.run("cd "+ new_edited_dir, shell=True, capture_output=True, text=True)
            output_chmod= subprocess.run("sudo chmod 777 db.sqlite3 ", shell=True, capture_output=True, text=True)


        file = open('/etc/nginx/sites-available/Internet-engineering-proj/Internet-engineering-proj.conf','r+')
        replaced_content = ""
        for line in file:
            new_line = line 

            if line.find(current_Dir) != -1:
                new_line = "/var/www/"+ new_dir + ";\n"

            replaced_content = replaced_content + new_line
        file.close()
        write_file = open('/etc/nginx/sites-available/Internet-engineering-proj/Internet-engineering-proj.conf', "w")

        write_file.write(replaced_content)
        write_file.close()
        return_data["change_directory"] = "the home directory successfully changed!"

        cmd_mail = "mutt -s 'Web server Stopped'  admin@UIIE.LOC <  /var/www/Mails/Mail_Web_Change_dir.txt"
        output = subprocess.run(cmd_mail, shell=True, capture_output=True, text=True)

        return Response(return_data, status=200)

class ShowLogs(generics.GenericAPIView):
    permission_classes = [IsAuthenticated ,]
    def get(self , request):
        logs = getLogs(request.user)
        data1 = []
        for i in logs: 
            data = {}
            data['id'] = i[0]
            data['requested_at'] = i[1]
            data['response_ms'] = i[2]
            data['path'] = i[3]
            data['remote_addr'] = i[4]
            data['host'] = i[5]
            data['method'] = i[6]
            data['query_params'] = i[7]
            data['data'] = i[8]
            data['response'] = i[9]
            data['status_code'] = i[10]
            data['user_id'] = i[11]
            data['view'] = i[12]
            data['view_method'] = i[13]
            data['errors'] = i[14]
            data['username_persistent'] = i[15]
            data1.append(data)
        return Response(data1)
        
def getLogs(user):

    database = r"db.sqlite3"
    connection = None
    try:
        connection = sqlite3.connect(database)
    except Error as e:
        print(e)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM rest_framework_tracking_apirequestlog")
    userLogs = []
    logs = cursor.fetchall()
    if user.is_superuser == 1:
        for i in logs:
            userLogs.append(i)
    else:
        for i in logs:
            if (i[15] == user.username):
                userLogs.append(i)
    return userLogs
   
