# urls.py
from django.urls import path
from .dashboard import(
    DashboardDataViewSet
)
from .masters import(
    SystemConfigurationAPIView, SystemIpPoolAPIView,
)
from .reports import(
    LogsAPIView,
)

urlpatterns = [
    path('dashboard/', DashboardDataViewSet.as_view({'get': 'list'}), name='dashboard'),   

    path('systemconfig/', SystemConfigurationAPIView.as_view({'get': 'list','post': 'create'}), name='system_configuration'),
    path('systemconfig/<int:id>/', SystemConfigurationAPIView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}), name='system_configuration'),

    path('systemippool/', SystemIpPoolAPIView.as_view({'get': 'list','post': 'create'}), name='system_ip_pool'),
    path('systemippool/<int:id>/', SystemIpPoolAPIView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}), name='system_ip_pool'),

    path('logs/', LogsAPIView.as_view({'get': 'list'}), name='logs'),
]