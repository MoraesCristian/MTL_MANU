from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "Por favor, insira o email e a senha")
            return redirect('contact:login')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email ou senha inválidos")
            return redirect('login')
    
    return render(request, 'contact/login.html')

@login_required
def home_view(request):
    return render(request, 'contact/home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'contact/password_reset.html'