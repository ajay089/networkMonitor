from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.authtoken.models import Token
from networkMonitor.decorators import unauthenticated_user

@unauthenticated_user
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            if not username and not password:
                messages.error(request, f'Please enter username and password.', extra_tags='invalid')
            elif not username:
                messages.error(request, f'Please enter username.', extra_tags='invalid')
            elif not password:
                messages.error(request, f'Please enter password.', extra_tags='invalid')
            
            # Reset entered values by re-rendering the form with an empty context
            return render(request, 'auth/index.html', {'username': username if username else '', 'password': ''})

        user = authenticate(request, username=username, password=password)
     
        if user is not None:
            login(request, user)
            
            # Fetch the token for the authenticated user
            token, created = Token.objects.get_or_create(user=request.user)

            username = f"{user.username}"
            request.session['username'] = username
            messages.success(request, f'Hello '+username+', Welcome to Era Network Dashbaord!')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('dashboard')  # Change 'home' to the URL you want to redirect to after login
        else:
            messages.error(request, f'Invalid username or password.', extra_tags='invalid')
            return redirect('login')
    return render(request, 'auth/index.html')  # Change 'login.html' to the template you're using for login


def logout_view(request):
    try:
        messages.success(request, f'You have successfully logout!', extra_tags='success')
        user = request.user
        # Retrieve the token associated with the user
        try:
            token = Token.objects.get(user=user)
            token.delete()  # Delete the token
        except Token.DoesNotExist:
            pass  # Token does not exist
        
        logout(request)
    except Exception as e:
        print(e)
    return redirect('login')

def handler403(request, exception):
    return redirect('login')  

def error_404_view(request, exception):
    return render(request, 'auth/404.html', status=404)       