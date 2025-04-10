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
from django.utils import timezone
from datetime import timedelta

from django.contrib.messages import get_messages
from django.http import JsonResponse

from main.utils import ValidarUsuarioContraseña as vuc
from main.servicio import servicioClientes as sc
from main.utils import GenerarCodigoAleatorio as gca

from main.repositorio import repositorioMembresia as rm
from main.repositorio import repositorioCliente as rc

from .models import Cliente, Producto
from django.shortcuts import render, redirect
from django.contrib import messages

#Las vistas de todo el sistema

#Vista para la pagina principal
def index(request):
    notificaciones = obtener_notificaciones()
    return render(request, 'inicio.html', {
        'notificaciones': notificaciones,
    })

def inicio_view(request):
    return render(request, 'index.html')

#Vista para la pagina de inicio de sesion
def signin_view(request):

    #Procesar y limpiar los mensajes
    storage=get_messages(request)

    for _ in storage:
        pass #eliminacion de mensajes

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validar si el nombre de usuario es incorrecto
        if not vuc.validarNombreUsuario(username):
            if not vuc.validarContraseña(username, password):  # Si también la contraseña es incorrecta
                messages.error(request, 'El usuario y la contraseña son incorrectos.')
            else:
                messages.error(request, 'El usuario no existe.')
            return redirect('signin')

        # Validar si la contraseña es incorrecta
        if not vuc.validarContraseña(username, password):
            messages.error(request, 'La contraseña es incorrecta.')
            return redirect('signin')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            print("Se logro")
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('inicio')
        else:
            return redirect('signin')
    return render(request, 'signin.html')

def logout_view(request):
    print("Estoy cerrando")
    logout(request)
    messages.success(request, 'Nos vemos pronto', extra_tags='success|Cierre de sesion exitoso')
    return redirect('inicio.html')

def clientes_view(request):

    if request.method == 'POST':

        # Procesar el formulario enviado desde el modal
        nombre_cliente = request.POST.get('nombre')
        sexo = request.POST.get('sexo')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        nombre_membresia = request.POST.get('membresia')  # Nombre de la membresía enviado desde el formulario
        fecha_inicio = request.POST.get('fecha_inicio')

        valido, mensaje = sc.validarCamposVacios(
            nombre_cliente, fecha_nacimiento, sexo, timezone.now()
        )
        if not valido:
            return JsonResponse({
                'InformacionAceptada': False,
                'message': mensaje
            })
        # Busca la membresía en la base de datos por nombre
        membresia = rm.obtenerMembresiaPorNombre(nombre_membresia)

        # Validar la fecha de nacimiento
        valido, mensaje = sc.validarFechaNacimiento(fecha_nacimiento)
        if not valido:
            
            return JsonResponse({
                'message': mensaje,
                'InformacionAceptada': False
            })

        rc.crearCiente(
            nombre=nombre_cliente,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            fecha_inicio=fecha_inicio,  # Fecha de inicio de membresía actual
            membresia=membresia
        )

        # Respuesta de éxito
        return JsonResponse({
            'message': 'Cliente registrado exitosamente.',
            'InformacionAceptada': True
        })
    
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        clientes = rc.UnirClienteMembresia()  # Obtener todos los clientes y sus membresías
        clientes_data = [
            {
                'id': cliente.id_cliente,
                'nombre': cliente.nombre_cliente,
                'sexo': cliente.sexo,
                'fecha_nacimiento': cliente.fecha_nacimiento,
                'membresia': cliente.membresia.nombre,
                'estado': cliente.estado,
                'fecha_inicio': cliente.fecha_inicio,
            }
            for cliente in clientes
        ]
        return JsonResponse({'clientes': clientes_data})

    # Si es una solicitud GET, renderizar la página con los datos necesarios
    clientes = rc.UnirClienteMembresia()  # Obtener todos los clientes y sus membresías
    membresias = rm.obtenerMembresias()  # Obtener todas las membresías de la base de datos
    opciones_sexo = rc.obtenerOpcionesSexo()  # Obtener las opciones de sexo definidas en el modelo Cliente
    return render(request, 'clientes.html', {
        'clientes': clientes,
        'membresias': membresias,
        'opciones_sexo': opciones_sexo,
    })


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
    if request.method == 'Post':
        print("Procesando el formulario")
        pass

    
    return render(request, 'registro_clientes.html')

@login_required
def asistencia_view(request):
    return render(request, 'asistencia.html')


def registro_productos_view(request):
    return render(request, 'registro_productos.html')


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

#vista para las notificiones

def obtener_notificaciones():
    hoy = timezone.now().date()
    notificaciones = []

    clientes = Cliente.objects.filter(fecha_inicio__isnull=False, membresia__isnull=False)

    for cliente in clientes:
        fecha_inicio = cliente.fecha_inicio
        duracion = cliente.membresia.duracion or 0
        fecha_fin = fecha_inicio + timedelta(days=duracion)

        if fecha_fin < hoy:
            notificaciones.append({
                "titulo": f"Membresía vencida",
                "mensaje": f"{cliente.nombre_cliente} venció el {fecha_fin.strftime('%d/%m/%Y')}.",
                "icono": "alert-circle",  # ícono de Feather
                "tipo": "danger"
            })
        elif fecha_fin == hoy:
            notificaciones.append({
                "titulo": f"Vence hoy",
                "mensaje": f"La membresía de {cliente.nombre_cliente} vence hoy.",
                "icono": "clock",
                "tipo": "info"
            })
        elif fecha_fin == hoy + timedelta(days=1):
            notificaciones.append({
                "titulo": f"Vence mañana",
                "mensaje": f"La membresía de {cliente.nombre_cliente} vence mañana.",
                "icono": "alert-triangle",
                "tipo": "info"
            })
    return notificaciones


