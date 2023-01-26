from django.urls import path
from . import views




urlpatterns = [

    path('register/', views.Register.as_view(), name='user_register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('showLog/', views.ShowLogs.as_view(), name='showLog'),
    # path('dhcp/', views.DhcpConfig.as_view(), name='dhcp'),
    path('dhcp/start/', views.DhcpConfigStart.as_view(), name='dhcp_start'),
    path('dhcp/stop/', views.DhcpConfigStop.as_view(), name='dhcp_stop'),
    path('dhcp/changeIpRange/', views.DhcpConfigChangeIpRange.as_view(), name='dhcp_change_ip_range'),
    path('dhcp/status/', views.DhcpConfigStatus.as_view(), name='dhcp_status'),
    #Mail configuration
    path('mail/start/', views.MailConfigStart.as_view(), name='mail_start'),
    path('mail/stop/', views.MailConfigStop.as_view(), name='mail_stop'),
    path('mail/status/', views.MailConfigStatus.as_view(), name='mail_status'),
    #Web Server Configuration
    path('web/start/', views.WebServerConfigStart.as_view(), name='web_start'),
    path('web/stop/', views.WebServerConfigStop.as_view(), name='web_stop'),
    path('web/status/', views.WebServerConfigStatus.as_view(), name='web_status'),


    
]