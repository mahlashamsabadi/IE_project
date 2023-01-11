from django.urls import path
from . import views




urlpatterns = [

    path('register/', views.Register.as_view(), name='user_register'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('dhcp/', views.DHCPConfig.as_view(), name='dhcp'),
]