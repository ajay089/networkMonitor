# urls.py
from django.urls import path
from .dashboard import(
    DashboardDataViewSet
)
from .masters import(
    SystemConfigurationAPIView
)

urlpatterns = [
    path('dashboard/', DashboardDataViewSet.as_view({'get': 'list'}), name='dashboard'),   
    path('systemconfig/', SystemConfigurationAPIView.as_view({'get': 'list','post': 'create'}), name='system_configuration'),
    path('systemconfig/<int:id>/', SystemConfigurationAPIView.as_view({'put': 'update', 'get': 'retrieve'}), name='system_configuration'),
]