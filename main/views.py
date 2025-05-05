from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
import json

from django.contrib.messages import get_messages
from django.http import JsonResponse

from main.utils import ValidarUsuarioContraseña as vuc
from main.servicio import servicioClientes as sc
from main.servicio import servicioProducto as sp
from main.servicio import servicioPagos as spg
from main.servicio import servicioPagoDescuento as spd

from main.utils import GenerarCodigoAleatorio as gca

from main.repositorio import repositorioMembresia as rm
from main.repositorio import repositorioDescuento as rpd
from main.repositorio import repositorioCliente as rc
from main.repositorio.repositorioMembresiaCliente import RepositorioMembresiaCliente 
from main.repositorio import repositorioProductos as rp
from main.repositorio import repositorioPago as rpa

from django.shortcuts import render, redirect
from django.contrib import messages

from django.db import transaction

#Las vistas de todo el sistema

#Vista para la pagina principal
def index(request):
    return render(request, 'inicio.html')

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
        action = request.POST.get('action') or json.loads(request.body).get('action')

        if action == "filtrar_clientes":
            try:
                print("Recibiendo filtros desde el frontend")
                filtros = json.loads(request.body)

                # Verificar si no hay filtros seleccionados
                noFiltrosSeleccionados = (
                    not filtros.get("nombre") and
                    not filtros.get("sexo") and
                    not filtros.get("estado") and
                    not filtros.get("membresias")
                )

                if noFiltrosSeleccionados:
                    print("No se seleccionaron filtros, devolviendo todos los clientes")
                    clientes = sc.prepararVistaTodosLosClientes()
                    return JsonResponse({"clientes": clientes})

                # Aplicar filtros si hay alguno seleccionado
                clientes = []

                if "membresias" in filtros and filtros["membresias"]:
                    if "Diaria" in filtros["membresias"]:
                        clientes.extend(sc.prepararVistaClientesConMembresiaDiaria())
                    if "Semanal" in filtros["membresias"]:
                        clientes.extend(sc.prepararVistaClientesConMembresiaSemanal())
                    if "Quincenal" in filtros["membresias"]:
                        clientes.extend(sc.prepararVistaClientesConMembresiaQuincenal())
                    if "Mensual" in filtros["membresias"]:
                        clientes.extend(sc.prepararVistaClientesConMembresiaMensual())

                if filtros.get("estado"):
                    clientes = [c for c in clientes if c["membresia"] and c["membresia"]["estado"] in filtros["estado"]]

                if filtros.get("sexo"):
                    clientes = [c for c in clientes if c["sexo"] in filtros["sexo"]]

                if filtros.get("nombre"):
                    clientes = [c for c in clientes if filtros["nombre"].lower() in c["nombre_cliente"].lower()]

                return JsonResponse({"clientes": clientes})

            except Exception as e:
                print(f"Error al procesar los filtros: {str(e)}")
                return JsonResponse({"error": f"Error al procesar los filtros: {str(e)}"}, status=500)

        elif action == "todos_los_clientes":
            try:
                print("Preparando vista de todos los clientes")
                clientes = sc.prepararVistaTodosLosClientes()
                return JsonResponse({"clientes": clientes})
            except Exception as e:
                print(f"Error al obtener todos los clientes: {str(e)}")
                return JsonResponse({"error": f"Error al obtener todos los clientes: {str(e)}"}, status=500)

    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        clientes = rc.obtenerClientesConMembresiaActiva()
        return JsonResponse({'clientes': clientes})

    clientes = sc.prepararVistaTodosLosClientes()
    tipoMembresias = rm.obtenerMembresias()
    opciones_sexo = rc.obtenerOpcionesSexo()
    return render(request, 'clientes.html', {
        'clientes': clientes,
        'membresias': tipoMembresias,
        'opciones_sexo': opciones_sexo,
    })

def productos_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_producto = request.POST.get('nombre').strip()
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad').strip()
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        estado = request.POST.get('estado')

        # Convertir los valores numéricos
        try:
            precio = float(precio) if precio else None
            cantidad = int(cantidad) if cantidad else None
        except ValueError:
            messages.error(request, 'El precio debe ser un número y la cantidad debe ser un entero.')
            return redirect('productos')

        # Registrar el producto utilizando las validaciones centralizadas
        valido, mensaje = sp.registrarProducto(
            nombre_producto=nombre_producto,
            precio=precio,
            descripcion=descripcion,
            fecha_ingreso=fecha_ingreso,
            existencia=cantidad,
            tipo=tipo,
            estado=estado
        )

        if not valido:
            messages.error(request, mensaje)
            return redirect('productos')

        # Respuesta de éxito
        messages.success(request, mensaje)

    # Manejar solicitudes AJAX para obtener la lista de productos
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        productos = rp.obtenerProductos()  # Obtener todos los productos de la base de datos
        productos_data = [
            {
                'id': producto.id,
                'nombre_producto': producto.nombre_producto,
                'precio': producto.precio,
                'descripcion': producto.descripcion,
                'fecha_ingreso': producto.fecha_ingreso,
                'existencia': producto.existencia,
                'tipo': producto.tipo,
                'estado': producto.estado,
            }
            for producto in productos
        ]
        return JsonResponse({'productos': productos_data})

    # Obtener los productos y tipos para renderizar la página
    productos = rp.obtenerProductos()  # Obtener todos los productos de la base de datos
    tipos = rp.obtenerTiposDeProductos()  # Obtener todos los tipos de productos de la base de datos
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


