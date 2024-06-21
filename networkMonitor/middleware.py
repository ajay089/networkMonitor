from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import logout

class Redirect403Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 403:
            return redirect('login')
        elif response.status_code == 500:
            logout(request)
            return redirect('login')  
        return response