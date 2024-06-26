import requests
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from apps.backend.models import(
    Department
)

@method_decorator(login_required, name='dispatch')
class SystemConfigurationView(View):
    template = 'master/system_configuration/index.html'
    form_template_name = 'master/system_configuration/add_edit.html'

    def get(self, request, *args, **kwargs):
        if 'type' in request.GET and request.GET['type'] == 'add':
            try:
                # Fetch the 'id' from GET parameters
                id = request.GET.get('id')
                api_url = f"{settings.API_BASE_URL}/api/systemconfig/"
                token = f'Token {request.user.auth_token}'
                
                # Set the page title based on the presence of 'id' in the GET parameters
                if id:
                    page_title = 'Edit System Configuration'
                    api_url += f'{id}/'
                    headers = {
                        'Authorization': token
                    }

                    # Making the GET request to the API
                    response = requests.get(api_url, headers=headers)
                    # Handling the response
                    if response.status_code == 200:
                        context = {
                            'page_title': page_title,
                            'api_url': api_url,
                            'token': token,
                            'result': response.json()
                        }
                        
                        return render(request, self.form_template_name, context)
                    else:
                        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
                    
                else:
                    page_title = 'Add System Configuration'
                

                    context = {
                        'page_title': page_title,
                        'api_url': api_url,
                        'token': token
                    }
                    
                    return render(request, self.form_template_name, context)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)    
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

@method_decorator(login_required, name='dispatch')
class SystemIpPoolView(View):
    template = 'master/system_ip_pool/index.html'
    form_template_name = 'master/system_ip_pool/add_edit.html'

    def get(self, request, *args, **kwargs):
        if 'type' in request.GET and request.GET['type'] == 'add':
            try:
                departments = Department.objects.filter().order_by('department_name')
                print(departments)

                # Fetch the 'id' from GET parameters
                id = request.GET.get('id')
                api_url = f"{settings.API_BASE_URL}/api/systemippool/"
                token = f'Token {request.user.auth_token}'
                
                # Set the page title based on the presence of 'id' in the GET parameters
                if id:
                    page_title = 'Edit System IP Pool Range'
                    api_url += f'{id}/'
                    headers = {
                        'Authorization': token
                    }

                    # Making the GET request to the API
                    response = requests.get(api_url, headers=headers)
                    # Handling the response
                    if response.status_code == 200:
                        context = {
                            'page_title': page_title,
                            'api_url': api_url,
                            'token': token,
                            'departments':departments,
                            'result': response.json()
                        }
                        
                        return render(request, self.form_template_name, context)
                    else:
                        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
                    
                else:
                    page_title = 'Add System IP Pool Range'
                

                    context = {
                        'page_title': page_title,
                        'departments':departments,
                        'api_url': api_url,
                        'token': token
                    }
                    
                    return render(request, self.form_template_name, context)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)    
        else:
            departments = Department.objects.filter().order_by('department_name')
            # List system IP Pools
            api_url = f"{settings.API_BASE_URL}/api/systemippool/"
            token = f'Token {request.user.auth_token}'
        
            context = {
                'page_title': 'System IP Pool',
                'departments':departments,
                'api_url': api_url,
                'token': token
            }
            
            return render(request, self.template, context)        
        
