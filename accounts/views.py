from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from rest_framework_tracking.mixins import LoggingMixin
from permissions import *
from rest_framework import generics

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
    def handle_log(self):
         print(self.log['user'])
         return self.log['user']

        