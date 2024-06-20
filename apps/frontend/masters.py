from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class SystemConfigurationView(View):
    template = 'master/system_configuration/index.html'
    form_template_name = 'master/system_configuration/add_edit.html'

    def get(self, request, *args, **kwargs):
        if 'type' in request.GET and request.GET['type'] == 'add':
            page_title = 'Edit System Configuration' if id in request.GET else 'Add System Configuration'
    
            # List system configurations
            api_url = f"{settings.API_BASE_URL}/api/systemconfig/"
            token = f'Token {request.user.auth_token}'

            context = {
                'page_title': page_title,
                'api_url': api_url,
                'token': token
            }
            
            return render(request, self.form_template_name, context)
        else:
            # List system configurations
            api_url = f"{settings.API_BASE_URL}/api/systemconfig/"
            token = f'Token {request.user.auth_token}'
        
            context = {
                'page_title': 'System Configuration',
                'api_url': api_url,
                'token': token
            }
            
            return render(request, self.template, context)
        
