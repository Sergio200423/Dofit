from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sessions.models import Session

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

from django.db import transaction

from main.servicio.servicioPagoDescuento import registrarPagoDescuentos  # Importar el servicio

def clientes_view(request):
    if request.method == 'POST':
        try:
            # Procesar el formulario enviado desde el modal
            nombre_cliente = request.POST.get('nombre')
            sexo = request.POST.get('sexo')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            nombre_membresia = request.POST.get('membresia')  # Nombre de la membresía enviado desde el formulario
            fecha_registro = request.POST.get('fecha_registro')
            carnet_estudiante = request.POST.get('carnet_estudiante')  # Nuevo campo para el carnet de estudiante

            print(f"Datos recibidos: {nombre_cliente}, {sexo}, {fecha_nacimiento}, {nombre_membresia}, {fecha_registro}, {carnet_estudiante}")

            # Busca la membresía en la base de datos por nombre
            membresia = rm.obtenerMembresiaPorNombre(nombre_membresia)

            if not membresia:
                print(f"Error: No se encontró la membresía con el nombre '{nombre_membresia}'")
                return JsonResponse({
                    'InformacionAceptada': False,
                    'message': f"No se encontró la membresía con el nombre '{nombre_membresia}'."
                })

            print(f"Membresía encontrada: {membresia}")

            # Usar una transacción atómica para garantizar consistencia
            with transaction.atomic():
                # Registrar cliente utilizando las validaciones centralizadas
                valido, mensaje = sc.registrarClientes(
                    nombre=nombre_cliente,
                    fecha_nacimiento=fecha_nacimiento,
                    sexo=sexo,
                    fecha_registro=fecha_registro,
                    carnet_estudiante=carnet_estudiante  # Pasar el carnet de estudiante
                )

                if not valido:
                    print(f"Error al registrar cliente: {mensaje}")
                    return JsonResponse({
                        'InformacionAceptada': False,
                        'message': mensaje
                    })

                # Obtener el cliente recién creado
                cliente = rc.obtenerClientePorNombre(nombre_cliente)

                if not cliente:
                    print("Error: No se pudo encontrar el cliente recién registrado.")
                    return JsonResponse({
                        'InformacionAceptada': False,
                        'message': "No se pudo encontrar el cliente recién registrado."
                    })

                print(f"Cliente registrado: {cliente}")

                # Crear la membresía del cliente
                resultado_membresia = RepositorioMembresiaCliente.crear_membresia_cliente(
                    id_cliente=cliente.id_cliente,
                    id_membresia=membresia.id_membresia,
                    fecha_inicio=fecha_registro  # Usar la fecha de registro como fecha de inicio
                )

                if not resultado_membresia["success"]:
                    print(f"Error al crear la membresía: {resultado_membresia['error']}")
                    raise Exception(resultado_membresia["error"])

                print(f"Membresía creada: {resultado_membresia['membresia_cliente']}")

                # Registrar el pago de la membresía
                valido, mensaje_pago = spg.registrarPago(
                    tipo="Membresia",
                    fecha=fecha_registro,
                    cliente=cliente,
                    renovar_membresia=True
                )

                if not valido:
                    print(f"Error al registrar el pago: {mensaje_pago}")
                    raise Exception(mensaje_pago)

                print(f"Pago registrado correctamente para el cliente {cliente.nombre_cliente}")

                # Aplicar descuento si corresponde
                if carnet_estudiante:  # Verificar si el cliente tiene carnet de estudiante
                    descuento = rpd.obtenerDescuentoPorNombre("Estudiante")  # Obtener el descuento de estudiante
                    if descuento:
                        pago = rpa.obtenerUltimoPagoPorCliente(cliente)  # Obtener el último pago registrado
                        valido_descuento, mensaje_descuento = spd.registrarPagoDescuentos(pago, descuento)
                        if valido_descuento is True:
                            print(f"Descuento aplicado correctamente al pago del cliente {cliente.nombre_cliente}")
                        elif valido_descuento is None:
                            print(f"Advertencia: {mensaje_descuento}")  # No se aplicó el descuento, pero no es un error crítico
                        else:
                            print(f"Error al aplicar el descuento: {mensaje_descuento}")
                            raise Exception(mensaje_descuento)

            # Respuesta de éxito
            return JsonResponse({
                'message': "Cliente, membresía, pago y descuento registrados correctamente.",
                'InformacionAceptada': True
            })

        except Exception as e:
            # Capturar cualquier error y devolver un mensaje de error
            print(f"Error interno del servidor: {str(e)}")
            return JsonResponse({
                'InformacionAceptada': False,
                'message': f"Error interno del servidor: {str(e)}"
            })

    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        clientes = rc.obtenerClientesConMembresiaActiva()  # Obtener todos los clientes y sus membresías
        return JsonResponse({'clientes': clientes})

    # Si es una solicitud GET, renderizar la página con los datos necesarios
    clientes = rc.obtenerClientesConMembresiaActiva()  # Obtener todos los clientes y sus membresías
    tipoMembresias = rm.obtenerMembresias()  # Obtener todas las membresías de la base de datos
    opciones_sexo = rc.obtenerOpcionesSexo()  # Obtener las opciones de sexo definidas en el modelo Cliente
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


