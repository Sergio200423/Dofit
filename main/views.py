from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Agregar prints para verificar los datos ingresados
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('signin')
    return render(request, 'signin.html')


def logout_view(request):
    logout(request)
    return redirect('signin')

def signup_view(request):
    return render(request, 'signup.html')

@login_required
def clientes_view(request):
    return render(request, 'clientes.html')

@login_required
def productos_view(request):
    return render(request, 'productos.html')

def registro_clientes_view(request):
    return render(request, 'registro_clientes.html')


def asistencia_view(request):
    return render(request, 'asistencia.html')