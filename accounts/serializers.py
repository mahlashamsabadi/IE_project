from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, UntypedToken
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password' , 'type')
        extera_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class AddUserMailSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField()

class DhcpConfigChangeIpRangeMailSerializer(serializers.Serializer):
    startip = serializers.CharField(max_length=3)
    endip = serializers.CharField(max_length=3)

class DhcpConfigChangeIpRangeMailSerializer(serializers.Serializer):
    startip = serializers.CharField(max_length=100)
    endip = serializers.CharField()

class WebServerConfigChangeHomeDirSerializer(serializers.Serializer):
    newDirectory = serializers.CharField(max_length=100)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'username': self.user.username})
        
        if self.user.is_superuser:
          data.update({'type': "admin"})
        else:
            data.update({'type': self.user.type})  
        return data