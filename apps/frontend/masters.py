from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings


@login_required
def system_configuration(request):
    api_url = f"{settings.API_BASE_URL}/api/systemconfig/"
    token   = f'Token {request.user.auth_token}'
   
    context = {
        'page_title' : 'System Configuration',
        'api_url':api_url,
        'token':token
    }
    
    template     = 'master/system_configuration/index.html'
    return render(request, template, context)
