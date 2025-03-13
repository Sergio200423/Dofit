from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'Sergio' and password == '1234':
            # Simula el inicio de sesión exitoso
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('signin')
    return render(request, 'signin.html')

def signup_view(request):
    return render(request, 'signup.html')