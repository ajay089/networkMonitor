import requests
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.utils.decorators import method_decorator
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class LogView(View):
    template = 'reports/log_report.html'

    def get(self, request, *args, **kwargs):
        # List system configurations
        api_url = f"{settings.API_BASE_URL}/api/logs/"
        token = f'Token {request.user.auth_token}'
    
        context = {
            'page_title': 'Logs Report',
            'api_url': api_url,
            'token': token
        }
        
        return render(request, self.template, context)
                    
        
