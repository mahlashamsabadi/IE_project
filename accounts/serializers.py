from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, UntypedToken
class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email","password" , "username" , "type")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        # data.clear()
        # if self.user.shop_name == None:
        #     data.update({'type': 'user'})
        #     data.update({'username': self.user.username})
        # else:
        #     data.update({'type': 'seller'})
        #     data.update({'shop_name': self.user.shop_name})
        #     data.update({'shop_phone_number': self.user.shop_phone_number})

        # and everything else you want to send in the response
        data.update({'username': self.user.username})
        
        if self.user.is_superuser:
          data.update({'type': "admin"})
        else:
            data.update({'type': self.user.type})  
        return data