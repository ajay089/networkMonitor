# urls.py
from django.urls import path
from .dashbaord import(
    DashboardDataViewSet
)

urlpatterns = [
    path('dashboard/', DashboardDataViewSet.as_view({'get': 'list'}), name='dashboard'),   
]