from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class Redirect403Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 403:
            return redirect('login')  # Redirect to the login page
        return response