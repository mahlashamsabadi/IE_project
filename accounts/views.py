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
import subprocess
import json

class Register(LoggingMixin , generics.GenericAPIView):
    def post(self , request):
        srz_data = UserRegisterSerializer(data=request.POST)
        data={}
        if srz_data.is_valid():
            account = srz_data.save()
            data['username'] = account.username
            data['email'] = account.email
            data['type'] = account.type
            refresh = RefreshToken.for_user(account)
            data['access'] = str(refresh.access_token)
            return Response(data)
        return Response(srz_data.errors)

class CustomTokenObtainPairView(LoggingMixin, TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class DhcpConfigStart(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsDhcpManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        #change password
        pwd = "mahla_sh"
        cmd_start = "sudo service isc-dhcp-server start"
        output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)

        return_data["startError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)

        return Response(return_data)

class DhcpConfigStop(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsDhcpManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        #change password
        pwd = "mahla_sh"
        cmd_start = "sudo service isc-dhcp-server stop"
        output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)

        return_data["stopError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)


class DhcpConfigStatus(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsDhcpManager,]

    def get(self, request):

        return_data ={} 

        pwd = "mahla_sh"
        cmd_status = "sudo service isc-dhcp-server status"
        output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_status), shell=True, capture_output=True, text=True)


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



            PID_s = "" #؟؟

            index = s.find("Main PID: ") + 10
            while s[index]!= " " :
                PID_s += s[index]
                index = index+1


            return_data["Main PID"] =PID_s

        return_data = json.dumps(return_data, indent = 4)
        return Response(return_data)




class DhcpConfigChangeIpRange(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsDhcpManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return Response("helloooo")


class MailConfigStart(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsMailManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        #it should change to server password!
        pwd = "mahla_sh"
        cmd = "sudo /etc/init.d/postfix start"

        output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd), shell=True, capture_output=True, text=True)

        return_data ={}
        return_data["startOutput"] = output.stdout
        return_data["startError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)
        return Response(return_data)

class MailConfigStop(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsMailManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        #it should change to server password!
        pwd = "mahla_sh"
        cmd = "sudo /etc/init.d/postfix stop"

        output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd), shell=True, capture_output=True, text=True)
        return_data ={} 
        return_data["stopOutput"] = output.stdout
        return_data["stopError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)
        return Response(return_data)


class MailConfigStatus(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsMailManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data ={} 

        output = subprocess.run('systemctl status postfix', shell=True, capture_output=True, text=True)

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



            PID_s = ""

            index = s.find("Main PID: ") + 10
            while s[index]!= " " :
                 PID_s += s[index]
                 index = index+1


            return_data["Main PID"] =PID_s

            CPU_s = ""

            index = s.find("CPU: ") + 5
            while s[index]!= "\n" :
                 CPU_s += s[index]
                 index = index+1


            return_data["CPU"] =CPU_s

        return_data = json.dumps(return_data, indent = 4)
        return Response(return_data)

class WebServerConfigStart(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsWebManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        #change password
        pwd = "mahla_sh"
        cmd_start = "sudo systemctl start nginx"
        output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)

        return_data["startError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)

        return Response(return_data)

class WebServerConfigStop(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsWebManager,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return_data = {}
        #change password
        pwd = "mahla_sh"
        cmd_start = "sudo systemctl stop nginx"
        output = subprocess.run('echo {} | sudo -S {}'.format(pwd, cmd_start), shell=True, capture_output=True, text=True)

        return_data["stopError"] = output.stderr
        return_data = json.dumps(return_data, indent = 4)


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
   
