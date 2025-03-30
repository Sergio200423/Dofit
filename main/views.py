from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
from main.utils import GenerarCodigoAleatorio as gca
from django.contrib.messages import get_messages
from main.utils import ValidarUsuarioContraseña as vuc

from .models import Cliente
from .models import Producto
from .models import Membresia

#Las vistas de todo el sistema


#Vista para la pagina principal
def index(request):
    return render(request, 'index.html')


#Vista para la pagina de inicio de sesion
def signin_view(request):

    #Procesar y limpiar los mensajes
    storage=get_messages(request)

    for _ in storage:
        pass #eliminacion de mensajes

    
    # # Obtener el contador de intentos fallidos de la sesión
    # failed_attempts = request.session.get('failed_attempts', 0)
    # lockout_time = request.session.get('lockout_time')

    # # Verificar si el usuario está bloqueado
    # if lockout_time:
    #     lockout_time = timezone.datetime.fromisoformat(lockout_time)
    #     if timezone.now() < lockout_time:
    #         messages.error(request, 'Demasiados intentos fallidos. Inténtalo de nuevo más tarde.')
    #         return redirect('signin')
    #     else:
    #         # Restablecer el contador y el tiempo de bloqueo después de que expire el tiempo de bloqueo
    #         request.session['failed_attempts'] = 0
    #         request.session['lockout_time'] = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not vuc.validarNombreUsuario(username):
            messages.error(request, 'El usuario no existe.')
            return redirect('signin')

        # Validar si la contraseña es correcta
        if not vuc.validarContraseña(username, password):
            messages.error(request, 'La contraseña es incorrecta.')
            return redirect('signin')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            # Restablecer el contador de intentos fallidos después de un inicio de sesión exitoso
            request.session['failed_attempts'] = 0
            return redirect('index')
        else:
            # # Incrementar el contador de intentos fallidos
            # # failed_attempts += 1
            # # request.session['failed_attempts'] = failed_attempts

            # # if failed_attempts >= 3:
            # #     # Bloquear el acceso durante 5 minutos después de 3 intentos fallidos
            # #     lockout_time = timezone.now() + timedelta(minutes=5)
            # #     request.session['lockout_time'] = lockout_time.isoformat()
            #     messages.error(request, 'Demasiados intentos fallidos. Inténtalo de nuevo en 5 minutos.')
            # else:
            #     messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('signin')
    return render(request, 'signin.html')

def logout_view(request):
    logout(request)
    messages.error(request, 'Nos vemos pronto')
    return redirect('signin')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente, Membresia

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente, Membresia

def clientes_view(request):
    if request.method == 'POST':
        # Procesar el formulario enviado desde el modal
        nombre = request.POST.get('nombre')
        sexo = request.POST.get('sexo')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        nombre_membresia = request.POST.get('membresia')  # Nombre de la membresía enviado desde el formulario

        # Busca la membresía en la base de datos por nombre
        membresia = Membresia.objects.filter(nombre=nombre_membresia).first()

        # Crear un nuevo cliente
        Cliente.objects.create(
            nombre_cliente=nombre,
            sexo=sexo,
            fecha_nacimiento=fecha_nacimiento,
            membresia=membresia,  # Asigna la membresía encontrada
            fecha_inicio=timezone.now().date()  # Establece la fecha de inicio como la fecha actual
        )

        # Mostrar un mensaje de éxito
        messages.success(request, 'Cliente registrado exitosamente.')

        # Redirigir a la misma página para evitar reenvío de formulario
        return redirect('clientes')

    # Si es una solicitud GET, renderizar la página con los datos necesarios
    clientes = Cliente.objects.select_related('membresia').all()
    membresias = Membresia.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes, 'membresias': membresias})


def productos_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre').strip()
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad').strip()
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')
        fecha_ingreso = request.POST.get('fecha_ingreso')

        if not nombre or not precio or not cantidad or not descripcion or not tipo or not fecha_ingreso:
            # Si algún campo está vacío, muestra un mensaje de error
            messages.error(request, 'Todos los campos son obligatorios.')
            print("Algun campo esta vacio")
            return redirect('productos')

        try:
            precio = float(precio)  # Validar que el precio sea un número
            cantidad = int(cantidad)  # Validar que la cantidad sea un número entero
        except ValueError:
            messages.error(request, 'El precio debe ser un número y la cantidad debe ser un entero.')
            return redirect('productos')

        print("Procesando el formulario")
        Producto.objects.create(
            nombre=nombre,
            precio=precio,
            cantidad=cantidad,
            descripcion=descripcion,
            tipo=tipo,
            fecha_ingreso=fecha_ingreso
        )

        messages.success(request, 'Producto registrado exitosamente.')

    productos = Producto.objects.all()
    tipos = Producto.TIPOS
    return render(request, 'productos.html', {'productos': productos, 'tipos': tipos})

def maquinas_view(request):
    return render(request, 'maquinas.html')

def pagos_view(request):
    return render(request, 'pagos.html')

def registro_pagos_view(request):
    return render(request, 'registro_pagos.html')

def registro_clientes_view(request):
    if request.method == 'POST':

        print("procesando el formulario")
        # Procesa el formulario
        pass

    # Depuración: imprime las membresías en la consola
    membresias = Membresia.objects.all()
    print(membresias)  # Esto imprimirá las membresías en la consola
    return render(request, 'registro_clientes.html', {'membresias': membresias})

@login_required
def asistencia_view(request):
    return render(request, 'asistencia.html')


def registro_productos_view(request):
    if request.method == 'POST':
        
        print("Procesando el formulario")
        pass

    productos = Producto.objects.all()
    tipos = Producto.TIPOS
    return render(request, 'registro_productos.html', {'productos': productos, 'tipos': tipos})


def recuperar_contraseña_view(request):
    #Validamos si el metodo es POST
    if request.method == 'POST':
        #Obtenemos el correo del usuario ingresado por el usuario
        correo = request.POST.get('correo')
        codigo = gca.generar_codigo_verificacion()

        storage=get_messages(request)

        for _ in storage:
            pass #eliminacion de mensajes

        request.session['correo_usuario'] = correo
        request.session['codigo_verificacion'] = codigo
        
        #Procesamos el correo con el modulo de python "send mail"
        resultado = send_mail(
            'Recuperar contraseña',
            f'Tu codigo de verificacion es: {codigo}',
            'sergiodanielxd2004@gmail.com',
            [correo],
            fail_silently=False,
        )

        if resultado > 0:
            messages.success(request, 'Correo enviado correctamente')
            return redirect('email_enviado')
        else:    
            messages.error(request, 'Error al enviar el correo')
            return redirect('recuperar_contra')
    return render(request, 'recuperar_contra.html')


def reenviar_correo_view(request):
    # Recuperamos el correo de la sesión
    correo = request.session.get('correo_usuario')
    codigo = request.session.get('codigo_verificacion')

    if correo:
        # Reenviamos el correo
        resultado = send_mail(
            'Recuperar contraseña',
            f'Tu codigo de verificacion es: {codigo}',
            'sergiodanielxd2004@gmail.com',
            [correo],
            fail_silently=False,
        )

        if resultado > 0:
            messages.success(request, 'Correo reenviado correctamente')
        else:
            messages.error(request, 'Error al reenviar el correo')
    else:
        messages.error(request, 'No se encontró un correo para reenviar')

    return redirect('email_enviado')

def recuperar_contra_password_view(request):
    #Validamos si el metodo es POST
    if request.method == 'POST':
        #Obtenemos el correo del usuario ingresado por el usuario
        correo = request.POST.get('correo')
        codigo = gca.generar_codigo_verificacion()

        request.session['correo_usuario'] = correo
        request.session['codigo_verificacion'] = codigo
        
        #Procesamos el correo con el modulo de python "send mail"
        resultado = send_mail(
            'Recuperar contraseña',
            f'Tu codigo de verificacion es: {codigo}',
            'sergiodanielxd2004@gmail.com',
            [correo],
            fail_silently=False,
        )

        if resultado > 0:
            return redirect('email_enviado')
        else:    
            messages.error(request, 'Error al enviar el correo')
            return redirect('recuperar_contra_password')
    return render(request, 'recuperar_contra_password.html')

def correo_enviado_view(request):
    if request.method == 'POST':
        messages.success(request, 'Correo enviado correctamente')
        # Asegúrate de que cada valor tenga un valor predeterminado si es None
        primer_numero = request.POST.get('primerNumero', '')
        segundo_numero = request.POST.get('segundoNumero', '')
        tercer_numero = request.POST.get('tercerNumero', '')
        cuarto_numero = request.POST.get('cuartoNumero', '')

        # Concatenar los valores
        codigo = primer_numero + segundo_numero + tercer_numero + cuarto_numero
        codigo = int(codigo)
        
        if codigo == request.session.get('codigo_verificacion'):
            # Si el código es correcto, redirige a la página de cambio de contraseña
            return redirect('nueva_contraseña')
        else:
            messages.error(request, 'Código incorrecto')
            print('Código incorrecto')
            return redirect('email_enviado')
    return render(request, 'email_enviado.html')

def nueva_contraseña_view(request):
    if request.method == 'POST':
        contra = request.POST.get('contraseña')
        confirmar_contra = request.POST.get('confirmar_contraseña')

        if contra != confirmar_contra:
            messages.error(request, 'Las contraseñas no coinciden')
        else:
            # Obtén el usuario (en este caso, el superusuario)
            user = User.objects.get(username='sergio')
            user.set_password(contra)  # Cambia la contraseña
            user.save()

            # Cierra todas las sesiones activas del usuario
            sessions = Session.objects.all()
            for session in sessions:
                data = session.get_decoded()
                if data.get('_auth_user_id') == str(user.id):
                    session.delete()

            messages.success(request, 'Contraseña actualizada correctamente. Todas las sesiones han sido cerradas.')
            return redirect('signin')
    return render(request, 'nueva_contraseña.html')


