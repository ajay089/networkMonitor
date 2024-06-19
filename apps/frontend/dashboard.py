import requests
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings


@login_required
def index(request):
    api_url = f"{settings.API_BASE_URL}/api/dashboard/"
    token   = f'Token {request.user.auth_token}'
   
    context = {
        'api_url': api_url,
        'token':token
    }
    template     = 'dashboard/index.html'
    return render(request, template, context)
