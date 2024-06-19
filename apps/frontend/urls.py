from django.urls import include, path
from . import views, auth, dashboard
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', auth.index, name='login'),
    path('login', auth.index, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('dashboard', dashboard.index, name='dashboard'),
]