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

class Register(LoggingMixin , generics.GenericAPIView):
    def post(self , request):
        srz_data = UserRegister(data=request.POST)
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


class DhcpConfig(LoggingMixin , generics.GenericAPIView):
    permission_classes = [IsDhcpManager ,]

    def get(self, request):
        self.check_object_permissions(request , request.user)
        return Response("helloooo")

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
    for i in logs:
        if (i[15] == user.username):
            userLogs.append(i)
    return userLogs
   
