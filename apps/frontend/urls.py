from django.urls import include, path
from . import (
    auth, dashboard, masters
) 

urlpatterns = [
    path('', auth.index, name='login'),
    path('login', auth.index, name='login'),
    path('logout/', auth.logout_view, name='logout'),

    path('dashboard', dashboard.index, name='dashboard'),
    path('system/config', masters.SystemConfigurationView.as_view(), name='system_configuration'),
    path('system/ippool', masters.SystemIpPoolView.as_view(), name='system_ip_pool'),
]