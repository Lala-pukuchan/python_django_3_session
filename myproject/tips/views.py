from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib.auth import logout as auth_logout


def homepage(request):
    return render(request, 'tips/homepage.html')

def register_view(request):
    # Redirect to home if already logged in
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Create User
            user = User.objects.create_user(username=username, password=password)
            # Login immediately after creation
            auth_login(request, user)
            messages.success(request, f'User {username} has been created and logged in.')
            return redirect('homepage')
        else:
            # Re-render the page with validation errors
            return render(request, 'tips/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'tips/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # If authentication is successful, form.user contains the User object
            user = form.user
            # Process login
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('homepage')
        else:
            return render(request, 'tips/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'tips/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('homepage')
