# urls.py
from django.urls import path
from .dashboard import(
    DashboardDataViewSet
)

urlpatterns = [
    path('dashboard/', DashboardDataViewSet.as_view({'get': 'list'}), name='dashboard'),   
]