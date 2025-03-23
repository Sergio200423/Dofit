from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

def signin_view(request):
    # Obtener el contador de intentos fallidos de la sesión
    failed_attempts = request.session.get('failed_attempts', 0)
    lockout_time = request.session.get('lockout_time')

    # Verificar si el usuario está bloqueado
    if lockout_time:
        lockout_time = timezone.datetime.fromisoformat(lockout_time)
        if timezone.now() < lockout_time:
            messages.error(request, 'Demasiados intentos fallidos. Inténtalo de nuevo más tarde.')
            return redirect('signin')
        else:
            # Restablecer el contador y el tiempo de bloqueo después de que expire el tiempo de bloqueo
            request.session['failed_attempts'] = 0
            request.session['lockout_time'] = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            # Restablecer el contador de intentos fallidos después de un inicio de sesión exitoso
            request.session['failed_attempts'] = 0
            return redirect('index')
        else:
            # Incrementar el contador de intentos fallidos
            failed_attempts += 1
            request.session['failed_attempts'] = failed_attempts

            if failed_attempts >= 3:
                # Bloquear el acceso durante 5 minutos después de 3 intentos fallidos
                lockout_time = timezone.now() + timedelta(minutes=5)
                request.session['lockout_time'] = lockout_time.isoformat()
                messages.error(request, 'Demasiados intentos fallidos. Inténtalo de nuevo en 5 minutos.')
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

@login_required
def registro_clientes_view(request):
    return render(request, 'registro_clientes.html')

@login_required
def asistencia_view(request):
    return render(request, 'asistencia.html')

@login_required
def registro_productos_view(request):
    return render(request, 'base.html')

def recuperar_contra_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username)

        if user is not None:
            user.set_password(password)
            user.save()
            return redirect('signin')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('signin')
        
    return render(request, 'recuperar_contra.html')

def recuperar_contra_password_view(request):
    return render(request, 'recuperar_contra_password.html')