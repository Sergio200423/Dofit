# DJANGO IMPORTS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.text import slugify
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from datetime import date, timedelta
from collections import defaultdict
import json
from django.db.models import Q, Count, Sum


# MODELOS
from .models import *

# REPOSITORIOS
from main.repositorio import repositorioMembresia as rm
from main.repositorio import repositorioDescuento as rpd
from main.repositorio import repositorioCliente as rc
from main.repositorio.repositorioMembresiaCliente import RepositorioMembresiaCliente
from main.repositorio import repositorioProductos as rp
from main.repositorio import repositorioPago as rpa
from main.repositorio import repositorioPagoDescuento as rpd
from main.repositorio import repositorioPagoProductos as rpp

# SERVICIOS
from main.servicio import servicioClientes as sc
from main.servicio import servicioProducto as sp
from main.servicio import servicioPagos as spg
from main.servicio import servicioPagoDescuento as spd
from main.servicio import servicioPagoProducto as spp

# UTILS
from main.utils import ValidarUsuarioContraseña as vuc
from main.utils import GenerarCodigoAleatorio as gca

from django.contrib.messages import get_messages

#Las vistas de todo el sistema

#Vista para la pagina principal
def index(request):
    return render(request, 'inicio.html')

def inicio_view(request):
    return render(request, 'dashboard.html')

#Vista para la pagina de inicio de sesion
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"[DEBUG] Username recibido: {username}")
        print(f"[DEBUG] Password recibido: {password}")

        try:
            user = Usuario.objects.get(nombre_usuario=username)
            n_intentos = user.n_intentos
            print(f"[DEBUG] Usuario encontrado en BD: {user.nombre_usuario}, hash: {user.contra}")
            print(f"[DEBUG] Intentos actuales: {n_intentos}")
            # Si el usuario ya está bloqueado
            if n_intentos >= 3:
                print(f"[DEBUG] Usuario {username} bloqueado por demasiados intentos")
                messages.error(request, 'Usuario bloqueado por demasiados intentos fallidos. Contacte al administrador.')
                return render(request, 'login.html', {'n_intentos': user.n_intentos})
            if (username == 'admin' and user.rol_id != 1) or (username == 'empleado' and user.rol_id != 2):
                print(f"[DEBUG] Rol incorrecto para {username}: {user.rol_id}")
                messages.error(request, 'El usuario no existe.')
                if user.n_intentos < 3:
                    user.n_intentos += 1
                    user.save()
                    print(f"[DEBUG] Intentos actuales: {user.n_intentos}")
                return render(request, 'login.html', {'n_intentos': user.n_intentos})
            
            if check_password(password, user.contra):
                user.n_intentos = 0
                user.save()
                print(f"[DEBUG] Password correcto para {username}")
                request.session['usuario_id'] = user.id_usuario
                request.session['usuario_nombre'] = user.nombre_usuario
                request.session['usuario_rol'] = user.rol.nombre
                # Redirigir al dashboard correcto
                return redirect('dashboard_empleado')
            else:
                print(f"[DEBUG] Password incorrecto para {username}")
                messages.error(request, 'Usuario o contraseña incorrecta')
                if user.n_intentos < 3:
                    user.n_intentos += 1
                    user.save()
                    print(f"[DEBUG] Intentos actuales: {user.n_intentos}")
                # Si después de incrementar ya está bloqueado, mostrar mensaje de bloqueo
                if user.n_intentos >= 3:
                    messages.error(request, 'Usuario bloqueado por demasiados intentos fallidos. Contacte al administrador.')
                return render(request, 'login.html', {'n_intentos': user.n_intentos})
        except Usuario.DoesNotExist:
            print(f"[DEBUG] Usuario {username} no existe en la BD")
            messages.error(request, 'El usuario no existe.')
            n_intentos = 0
        return render(request, 'login.html', {'n_intentos': n_intentos})
    return render(request, 'login.html', {'n_intentos': 0})

def logout_view(request):
    print("Estoy cerrando")
    logout(request)
    messages.success(request, 'Nos vemos pronto', extra_tags='success|Cierre de sesion exitoso')
    return redirect('inicio.html')


def clientes_view(request):

    if request.method == 'GET' and 'cliente_id' in request.GET:
        # Obtener los datos completos de un cliente
        cliente_id = request.GET.get('cliente_id')
        cliente = rc.obtenerClientePorId(cliente_id)
        if not cliente:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)

        # Obtener la membresía asociada al cliente desde la tabla intermedia
        try:
            membresia_cliente = RepositorioMembresiaCliente.obtener_membresia_activa(cliente_id)
            if membresia_cliente and membresia_cliente["success"]:
                membresia_nombre = membresia_cliente["membresia_activa"].membresia.nombreMembresia
            else:
                membresia_nombre = None
        except Exception as e:
            print(f"Error al obtener la membresía: {str(e)}")
            membresia_nombre = None

        return JsonResponse({
            "id": cliente.id_cliente,
            "nombre": cliente.nombre_cliente,
            "sexo": cliente.sexo,
            "fecha_nacimiento": cliente.fecha_nacimiento.strftime('%Y-%m-%d'),
            "membresia": membresia_nombre,
            "fecha_registro": cliente.fecha_registro.strftime('%Y-%m-%d'),
        })

    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        clientes = sc.prepararVistaTodosLosClientes()
        return JsonResponse({'clientes': clientes})

    # Renderizar la página con datos iniciales
    clientes = sc.prepararVistaTodosLosClientes()
    tipoMembresias = rm.obtenerMembresias()
    opciones_sexo = rc.obtenerOpcionesSexo()

    # Calcular los conteos para los pills
    membresia_counts = {
        'Diaria': sum(1 for c in clientes if c.get('membresia') and c['membresia'].get('nombreMembresia') == 'Diaria'),
        'Semanal': sum(1 for c in clientes if c.get('membresia') and c['membresia'].get('nombreMembresia') == 'Semanal'),
        'Quincenal': sum(1 for c in clientes if c.get('membresia') and c['membresia'].get('nombreMembresia') == 'Quincenal'),
        'Mensual': sum(1 for c in clientes if c.get('membresia') and c['membresia'].get('nombreMembresia') == 'Mensual'),
    }
    sexo_counts = {
        'M': sum(1 for c in clientes if c.get('sexo') == 'M'),
        'F': sum(1 for c in clientes if c.get('sexo') == 'F'),
    }
    estado_counts = {
        'activo': sum(1 for c in clientes if c.get('membresia') and c['membresia'].get('estado') == 'activo'),
        'inactivo': sum(1 for c in clientes if not c.get('membresia') or c['membresia'].get('estado') == 'inactivo'),
    }
    print('Conteos para pills:', membresia_counts, sexo_counts, estado_counts)
    return render(request, 'clientes.html', {
        'clientes': clientes,
        'membresias': tipoMembresias,
        'opciones_sexo': opciones_sexo,
        'membresia_counts': membresia_counts,
        'sexo_counts': sexo_counts,
        'estado_counts': estado_counts,
    })

def registrar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre_cliente = data.get('nombre_cliente')
            sexo = data.get('sexo')
            fecha_nacimiento = data.get('fecha_nacimiento')
            nombre_membresia = data.get('membresia')
            fecha_registro = data.get('fecha_registro')
            carnet_estudiante = data.get('carnet_estudiante')

            print(f"Datos recibidos: {nombre_cliente}, {sexo}, {fecha_nacimiento}, {nombre_membresia}, {fecha_registro}, {carnet_estudiante}")
            membresia = rm.obtenerMembresiaPorNombre(nombre_membresia)

            if not membresia:
                return JsonResponse({
                    'InformacionAceptada': False,
                    'message': f"No se encontró la membresía con el nombre '{nombre_membresia}'."
                })

            with transaction.atomic():
                # Registrar cliente
                valido, mensaje = sc.registrarClientes(
                    nombre=nombre_cliente,
                    fecha_nacimiento=fecha_nacimiento,
                    sexo=sexo,
                    fecha_registro=fecha_registro,
                    carnet_estudiante=carnet_estudiante
                )

                if not valido:
                    return JsonResponse({
                        'InformacionAceptada': False,
                        'message': mensaje
                    })

                # Obtener cliente recién registrado
                cliente = rc.obtenerClientePorNombre(nombre_cliente)

                if not cliente:
                    return JsonResponse({
                        'InformacionAceptada': False,
                        'message': "No se pudo encontrar el cliente recién registrado."
                    })

                # Registrar membresía del cliente
                resultado_membresia = RepositorioMembresiaCliente.crear_membresia_cliente(
                    id_cliente=cliente.id_cliente,
                    id_membresia=membresia.id_membresia,
                    fecha_inicio=fecha_registro
                )

                if not resultado_membresia["success"]:
                    raise Exception(resultado_membresia["error"])

                # Registrar pago
                valido, mensaje_pago = spg.registrarPago(
                    tipo="Membresia",
                    fecha=fecha_registro,
                    cliente=cliente,
                    renovar_membresia=True
                )

                if not valido:
                    raise Exception(mensaje_pago)

                # Registrar descuento si aplica
                if carnet_estudiante:
                    descuento = rpd.obtenerDescuentoPorNombre("Estudiante")
                    if descuento:
                        pago = rpa.obtenerUltimoPagoPorCliente(cliente)
                        valido_descuento, mensaje_descuento = spd.registrarPagoDescuentos(pago, descuento)
                        if not valido_descuento:
                            raise Exception(mensaje_descuento)

            return JsonResponse({
                'message': "Cliente, membresía, pago y descuento registrados correctamente.",
                'InformacionAceptada': True
            })

        except Exception as e:
            print(f"Error interno del servidor: {str(e)}")
            return JsonResponse({"error": f"Error interno del servidor: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def filtrar_cliente(request):
    print("[DEBUG] Entrando a filtrar_cliente. Método:", request.method)
    if request.method == 'POST':
        try:
            print("[DEBUG] Body recibido:", request.body)
            data = json.loads(request.body)
            print("[DEBUG] Data decodificada:", data)

            # Normalizar filtros: si llegan como string, convertir a lista
            def to_list(val):
                if isinstance(val, list):
                    return val
                if val is None:
                    return []
                if isinstance(val, str):
                    return [val] if val else []
                return list(val)

            nombre = data.get("nombre", "")
            membresias = to_list(data.get("membresia", []))
            estado = to_list(data.get("estado", []))
            sexo = to_list(data.get("sexo", []))

            print(f"Filtros normalizados: nombre={nombre}, membresias={membresias}, estado={estado}, sexo={sexo}")

            # Obtener todos los clientes si no hay filtros
            if not (nombre or membresias or estado or sexo):
                clientes = sc.prepararVistaTodosLosClientes()
                return JsonResponse({"clientes": clientes})

            # Si hay filtros, empezar con todos los clientes y filtrar
            clientes = sc.prepararVistaTodosLosClientes()

            # Filtrar por membresía (si aplica)
            if membresias:
                clientes = [c for c in clientes if c.get("membresia") and c["membresia"].get("nombreMembresia") in membresias]

            # Filtrar por estado (si aplica)
            if estado:
                clientes = [c for c in clientes if c.get("membresia") and c["membresia"].get("estado") in estado]

            # Filtrar por sexo (si aplica)
            if sexo:
                clientes = [c for c in clientes if c.get("sexo") in sexo]

            # Filtrar por nombre (si aplica)
            if nombre:
                clientes = [c for c in clientes if nombre.lower() in c.get("nombre_cliente", "").lower()]

            return JsonResponse({"clientes": clientes})

        except Exception as e:
            print(f"[DEBUG] Error interno del servidor: {str(e)}")
            return JsonResponse({"error": f"Error interno del servidor: {str(e)}"}, status=500)

    print("[DEBUG] Método no permitido en filtrar_cliente")
    return JsonResponse({"error": "Método no permitido"}, status=405)

def editar_cliente(request, cliente_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            nombre_cliente = data.get('nombre_cliente')
            sexo = data.get('sexo')
            fecha_nacimiento = data.get('fecha_nacimiento')
            membresia = data.get('membresia')
            fecha_registro = data.get('fecha_registro')
            carnet_estudiante = data.get('carnet_estudiante')

            print(f"Datos recibidos para editar cliente: {cliente_id}, {nombre_cliente}, {sexo}, {fecha_nacimiento}, {fecha_registro}, {membresia}")

            # Validar que el cliente exista
            cliente = rc.obtenerClientePorId(cliente_id)
            if not cliente:
                return JsonResponse({
                    'InformacionAceptada': False,
                    'message': f"No se encontró el cliente con ID '{cliente_id}'."
                }, status=404)

            # Actualizar los datos del cliente
            valido, mensaje = rc.actualizarCliente(
                cliente_id=cliente_id,
                nombre=nombre_cliente,
                sexo=sexo,
                fecha_nacimiento=fecha_nacimiento,
            )
            if not valido:
                return JsonResponse({
                    'InformacionAceptada': False,
                    'message': mensaje
                }, status=400)

            # Actualizar la membresía del cliente si es necesario
            if membresia:
                membresia_activa = RepositorioMembresiaCliente.obtener_membresia_activa(cliente_id)

                if not membresia_activa["success"]:
                    return JsonResponse({
                        'InformacionAceptada': False,
                        'message': membresia_activa["error"]
                    }, status=400)

                id_membresia_cliente = membresia_activa["membresia_activa"].id_membresia_cliente

                nueva_membresia = rm.obtenerMembresiaPorNombre(membresia)

                if not nueva_membresia:
                    return JsonResponse({
                        'InformacionAceptada': False,
                        'message': f"No se encontró la membresía con el nombre '{membresia}'."
                    }, status=404)

                id_membresia = nueva_membresia.id_membresia

                resultado_membresia = RepositorioMembresiaCliente.actualizar_membresia_cliente(
                    id_membresia_cliente=id_membresia_cliente,
                    id_membresia=id_membresia
                )

                if not resultado_membresia["success"]:
                    return JsonResponse({
                        'InformacionAceptada': False,
                        'message': resultado_membresia["error"]
                    }, status=400)

            print(f"Cliente actualizado: nombre={cliente.nombre_cliente}, sexo={cliente.sexo}, fecha_nacimiento={cliente.fecha_nacimiento}, membresia={membresia}")
            return JsonResponse({
                'InformacionAceptada': True,
                'message': "Cliente actualizado correctamente.",
                'nombre_cliente': cliente.nombre_cliente,
                'sexo': cliente.sexo,
                'fecha_nacimiento': cliente.fecha_nacimiento.strftime('%Y-%m-%d') if cliente.fecha_nacimiento else '',
                'membresia': membresia,
            }, status=200)

        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {str(e)}")
            return JsonResponse({"error": "Datos JSON inválidos"}, status=400)

        except Exception as e:
            print(f"Error interno del servidor: {str(e)}")
            return JsonResponse({"error": f"Error interno del servidor: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def productos_view(request):
    """
    Vista para productos: responde con JSON si es petición AJAX/API, o HTML si es navegación normal.
    """
    productos = sp.prepararVistaProductos()
    tipos = Producto.TIPOS
    estados = Producto.ESTADOS

    # Asegurar que cada producto tenga la lista de estados para el renderizado inicial
    for producto in productos:
        producto['ESTADOS'] = estados

    # Normalizar tipos de productos para conteo robusto
    def normaliza_tipo(valor):
        return valor.strip().lower() if valor else ''

    tipos_validos = {normaliza_tipo(tipo[0]): tipo[0] for tipo in tipos}
    tipo_counts = {tipo[0]: 0 for tipo in tipos}
    tipos_no_validos = []
    for p in productos:
        tipo_prod = normaliza_tipo(p.get('tipo'))
        if tipo_prod in tipos_validos:
            tipo_counts[tipos_validos[tipo_prod]] += 1
        elif tipo_prod in [normaliza_tipo('Barra energética')]:
            tipo_counts['Barra energetica'] += 1
            tipos_no_validos.append(p.get('tipo'))
        else:
            tipos_no_validos.append(p.get('tipo'))

    estado_counts = {value: sum(1 for p in productos if p.get('estado') == value) for value, _ in estados}
    estados_conteo = [(value, label, estado_counts.get(value, 0)) for value, label in estados]
    total_productos = len(productos)
    total_en_stock = estado_counts.get('disponible', 0)
    total_pocas_unidades = estado_counts.get('pocas_unidades', 0)
    total_agotado = estado_counts.get('agotado', 0)
    
    # --- NUEVO: Si la petición es AJAX o la URL es /api/productos/, responde JSON ---
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/productos/'):
        return JsonResponse({
            'productos': productos,
            'tipos': list(tipos),
            'estados': list(estados),
            'estados_conteo': estados_conteo,
            'tipo_counts': tipo_counts,
            'barra_energetica_count': tipo_counts['Barra energetica'],
            'estado_counts': estado_counts,
            'total_productos': total_productos,
            'total_en_stock': total_en_stock,
            'total_pocas_unidades': total_pocas_unidades,
            'total_agotado': total_agotado,
        })

    # Si no, renderiza la página HTML como antes
    return render(request, 'productos.html', {
        'productos': productos,
        'tipos': tipos,
        'estados': estados,
        'estados_conteo': estados_conteo,
        'tipo_counts': tipo_counts,
        'barra_energetica_count': tipo_counts['Barra energetica'],
        'estado_counts': estado_counts,
        'total_productos': total_productos,
        'total_en_stock': total_en_stock,
        'total_pocas_unidades': total_pocas_unidades,
        'total_agotado': total_agotado,
    })


def filtrar_producto(request):
    """Filtra productos según los filtros recibidos por AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').lower()
            tipos = data.get('tipo', [])
            estados = data.get('estado', [])
            if isinstance(tipos, str):
                tipos = [tipos] if tipos else []
            if isinstance(estados, str):
                estados = [estados] if estados else []
            productos = sp.prepararVistaProductos()

            # Normalizar tipos para comparación robusta
            def normaliza_tipo(valor):
                return valor.strip().lower() if valor else ''
            tipos_normalizados = set([normaliza_tipo(t) for t in tipos])

            if tipos and 'Todos' not in tipos:
                productos = [p for p in productos if normaliza_tipo(p.get('tipo')) in tipos_normalizados]
            if estados:
                productos = [p for p in productos if p.get('estado') in estados]
            if nombre:
                productos = [p for p in productos if nombre in p.get('nombre_producto', '').lower()]

            # --- NUEVO: Recalcular contadores de tipo y estado con lógica robusta ---
            tipos_modelo = Producto.TIPOS
            tipos_validos = {normaliza_tipo(tipo[0]): tipo[0] for tipo in tipos_modelo}
            tipo_counts = {tipo[0]: 0 for tipo in tipos_modelo}
            for p in productos:
                tipo_prod = normaliza_tipo(p.get('tipo'))
                if tipo_prod in tipos_validos:
                    tipo_counts[tipos_validos[tipo_prod]] += 1
                elif tipo_prod in [normaliza_tipo('Barra energética')]:
                    tipo_counts['Barra energetica'] += 1
            barra_energetica_count = tipo_counts['Barra energetica']
            # Contadores de estado
            estados_modelo = Producto.ESTADOS
            estado_counts = {value: sum(1 for p in productos if p.get('estado') == value) for value, _ in estados_modelo}
            estados_conteo = [(value, label, estado_counts.get(value, 0)) for value, label in estados_modelo]

            return JsonResponse({
                'productos': productos,
                'tipo_counts': tipo_counts,
                'barra_energetica_count': barra_energetica_count,
                'estado_counts': estado_counts,
                'estados_conteo': estados_conteo,
                'total_productos': len(productos),
                'total_en_stock': estado_counts.get('disponible', 0),
                'total_pocas_unidades': estado_counts.get('pocas_unidades', 0),
                'total_agotado': estado_counts.get('agotado', 0),
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def registrar_producto(request):
    """Registra un nuevo producto vía AJAX"""
    if request.method == 'POST':
        try:
            print('DEBUG registrar_producto: request.content_type =', request.content_type)
            if request.content_type.startswith('multipart/form-data'):
                # Manejo de formulario con imagen
                print('DEBUG registrar_producto: POST keys =', list(request.POST.keys()))
                print('DEBUG registrar_producto: FILES keys =', list(request.FILES.keys()))
                # Cambiar a 'nombre_producto' para coincidir con el formulario
                nombre_producto = request.POST.get('nombre_producto')
                precio = request.POST.get('precio')
                cantidad = request.POST.get('existencia')
                descripcion = request.POST.get('descripcion')
                tipo = request.POST.get('tipo')
                fecha_ingreso = request.POST.get('fecha_ingreso')
                imagen = request.FILES.get('imagen')
                print(f"DEBUG registrar_producto: nombre={nombre_producto}, precio={precio}, cantidad={cantidad}, descripcion={descripcion}, tipo={tipo}, fecha_ingreso={fecha_ingreso}, imagen={imagen}")
                # Estado por defecto: disponible
                estado = 'disponible'
                valido, mensaje = sp.registrarProducto(
                    nombre_producto=nombre_producto,
                    precio=float(precio) if precio else None,
                    descripcion=descripcion,
                    fecha_ingreso=fecha_ingreso,
                    existencia=int(cantidad) if cantidad else None,
                    tipo=tipo,
                    imagen=imagen
                )
            else:
                print('DEBUG registrar_producto: JSON body')
                data = json.loads(request.body)
                nombre_producto = data.get('nombre_producto')
                precio = data.get('precio')
                cantidad = data.get('existencia')
                descripcion = data.get('descripcion')
                tipo = data.get('tipo')
                fecha_ingreso = data.get('fecha_ingreso')
                imagen = None
                print(f"DEBUG registrar_producto: nombre={nombre_producto}, precio={precio}, cantidad={cantidad}, descripcion={descripcion}, tipo={tipo}, fecha_ingreso={fecha_ingreso}")
                estado = 'disponible'
                valido, mensaje = sp.registrarProducto(
                    nombre_producto=nombre_producto,
                    precio=float(precio) if precio else None,
                    descripcion=descripcion,
                    fecha_ingreso=fecha_ingreso,
                    existencia=int(cantidad) if cantidad else None,
                    tipo=tipo,
                    imagen=imagen
                )
            if not valido:
                print('DEBUG registrar_producto: registro fallido:', mensaje)
                return JsonResponse({'InformacionValida': False, 'message': mensaje}, status=400)
            print('DEBUG registrar_producto: registro exitoso:', mensaje)
            return JsonResponse({'InformacionValida': True, 'message': mensaje}, status=200)
        except Exception as e:
            print('DEBUG registrar_producto: excepción:', str(e))
            return JsonResponse({'InformacionValida': False, 'message': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def editar_producto(request, producto_id):
    """Edita un producto existente vía AJAX"""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            nombre_producto = data.get('nombre_producto')
            precio = data.get('precio')
            existencia = data.get('existencia')
            descripcion = data.get('descripcion')
            tipo = data.get('tipo')
            # Aquí deberías tener una función en tu repositorio para actualizar el producto
            valido, mensaje = rp.actualizarProducto(
                producto_id=producto_id,
                nombre_producto=nombre_producto,
                precio=float(precio) if precio else None,
                existencia=int(existencia) if existencia else None,
                descripcion=descripcion,
                tipo=tipo,
            )
            if not valido:
                return JsonResponse({'InformacionValida': False, 'message': mensaje}, status=400)
            return JsonResponse({'InformacionValida': True, 'message': mensaje}, status=200)
        except Exception as e:
            return JsonResponse({'InformacionValida': False, 'message': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def pagos_view(request):
    # Si viene ?success=1 en la URL, mostrar mensaje de éxito
    if request.GET.get('success') == '1':
        from django.contrib import messages
        messages.success(request, '¡Compra realizada con éxito!')
    return render(request, 'pagos.html')

def reportePago_view(request):
    pagos = rpa.obtenerPagos().order_by('-fecha')
    pagos_context = []
    total_pagos = 0
    total_descuentos = 0
    total_productos = 0
    total_final = 0
    historial_fechas = []
    historial_totales = []
    pagos_semanal = defaultdict(float)
    pagos_mensual = defaultdict(float)
    pagos_anual = defaultdict(float)
    for pago in pagos:
        descuentos = rpd.obtenerDescuentosPorPago(pago)
        productos = rpp.obtenerPagoProductosPorPago(pago)
        suma_descuentos = sum([d.descuento.monto for d in descuentos])
        suma_productos = sum([p.cantidad for p in productos])
        total_pagos += pago.total_a_pagar
        total_descuentos += suma_descuentos
        total_productos += suma_productos
        total_final += pago.total_a_pagar - suma_descuentos
        historial_fechas.append(pago.fecha.strftime('%Y-%m-%d'))
        historial_totales.append(float(pago.total_a_pagar))
        year, week, _ = pago.fecha.isocalendar()
        pagos_semanal[f"{year}-S{week:02d}"] += float(pago.total_a_pagar)
        pagos_mensual[pago.fecha.strftime('%Y-%m')] += float(pago.total_a_pagar)
        pagos_anual[str(pago.fecha.year)] += float(pago.total_a_pagar)
        pagos_context.append({
            'id': pago.id_pago,
            'tipo': pago.tipo,
            'fecha': pago.fecha.strftime('%d/%m/%Y'),  # <-- Formato dd/mm/yyyy para mostrar en el template
            'cliente': pago.cliente.nombre_cliente if pago.cliente else '',
            'total_original': pago.total_a_pagar,
            'total_final': pago.total_a_pagar - suma_descuentos,
            'descuentos': [
                {
                    'nombre': d.descuento.nombre,
                    'monto': d.descuento.monto,
                    'descripcion': d.descuento.descripcion
                } for d in descuentos
            ],
            'productos': [
                {
                    'nombre': p.producto.nombre_producto,
                    'cantidad': p.cantidad,
                    'precio': p.producto.precio,
                    'total': p.total_a_pagar()
                } for p in productos
            ]
        })
    semanal_labels = sorted(pagos_semanal.keys())
    mensual_labels = sorted(pagos_mensual.keys())
    anual_labels = sorted(pagos_anual.keys())
    context = {
        # Pass pagos_context as a Python list for template iteration
        'pagos': pagos_context,
        # Only serialize to JSON the variables needed for JS
        'total_pagos': json.dumps(total_pagos),
        'total_descuentos': json.dumps(total_descuentos),
        'total_productos': json.dumps(total_productos),
        'total_final': json.dumps(total_final),
        'historial_fechas': json.dumps(historial_fechas[::-1]),
        'historial_totales': json.dumps(historial_totales[::-1]),
        'historial_semanal_labels': json.dumps(semanal_labels),
        'historial_semanal_data': json.dumps([pagos_semanal[k] for k in semanal_labels]),
        'historial_mensual_labels': json.dumps(mensual_labels),
        'historial_mensual_data': json.dumps([pagos_mensual[k] for k in mensual_labels]),
        'historial_anual_labels': json.dumps(anual_labels),
        'historial_anual_data': json.dumps([pagos_anual[k] for k in anual_labels]),
    }
    return render(request, 'reportePagos.html', context)

def registro_pagos_view(request):
    return render(request, 'registro_pagos.html')

def registro_clientes_view(request):
    if request.method == 'Post':
        print("Procesando el formulario")
        pass

    
    return render(request, 'registro_clientes.html')

def asistencia_view(request):
    return render(request, 'asistencia.html')


def registro_productos_view(request):
    return render(request, 'registro_productos.html')


def recuperar_contraseña_view(request):
    if request.method == 'POST':
        print('[DEBUG] Se recibió un POST en recuperar_contraseña_view')
        # Obtener el correo del usuario seleccionado desde el formulario
        correo = request.POST.get('correo')
        print(f'[DEBUG] Valor recibido en correo: {correo}')
        if correo:
            # Generar código de verificación
            codigo = gca.generar_codigo_verificacion()
            print(f'[DEBUG] Código generado: {codigo}')
            # Guardar en sesión
            request.session['correo_usuario'] = correo
            request.session['codigo_verificacion'] = codigo
            # Enviar correo
            try:
                resultado = send_mail(
                    'Recuperar contraseña',
                    f'Tu codigo de verificacion es: {codigo}',
                    'sergiodanielxd2004@gmail.com',
                    [correo],
                    fail_silently=False,
                )
                print(f'[DEBUG] Resultado de send_mail: {resultado}')
            except Exception as e:
                print(f'[DEBUG] Excepción al enviar correo: {e}')
                messages.error(request, f'Error al enviar el correo: {e}')
                return redirect('recuperar_contra')
            if resultado > 0:
                print('[DEBUG] Redirigiendo a email_enviado')
                return redirect('email_enviado')
            else:
                messages.error(request, 'Error al enviar el correo')
                print('[DEBUG] Error: send_mail retornó 0')
                return redirect('recuperar_contra')
        else:
            messages.error(request, 'No se seleccionó ningún usuario')
            print('[DEBUG] No se seleccionó ningún usuario')
            return redirect('recuperar_contra')
    # GET: mostrar la lista de usuarios
    usuarios = Usuario.objects.all()
    return render(request, 'recuperar_contra.html', {'usuarios': usuarios})

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

        # Nueva validación: la contraseña no debe ser igual a la actual
        correo_usuario = request.session.get('correo_usuario')
        if correo_usuario:
            try:
                usuario = Usuario.objects.get(correo=correo_usuario)
                if check_password(contra, usuario.contra):
                    messages.error(request, 'La nueva contraseña no puede ser igual a la actual.')
                    return render(request, 'nueva_contraseña.html', {"error_contra_igual": True})
            except Usuario.DoesNotExist:
                messages.error(request, 'No se encontró el usuario para actualizar la contraseña.')
                return render(request, 'nueva_contraseña.html')

        if contra != confirmar_contra:
            messages.error(request, 'Las contraseñas no coinciden')
        else:
            # Obtener el correo del usuario desde la sesión
            correo_usuario = request.session.get('correo_usuario')
            if correo_usuario:
                try:
                    usuario = Usuario.objects.get(correo=correo_usuario)
                    usuario.contra = make_password(contra)
                    usuario.n_intentos = 0  # Restablecer intentos fallidos al cambiar la contraseña
                    usuario.save()

                    # Cierra todas las sesiones activas del usuario (si aplica)
                    sessions = Session.objects.all()
                    for session in sessions:
                        data = session.get_decoded()
                        if data.get('usuario_id') == usuario.id_usuario:
                            session.delete()

                    # Limpiar mensajes antes de redirigir al login
                    storage = get_messages(request)
                    for _ in storage:
                        pass  # Consumir todos los mensajes

                    messages.success(request, 'Contraseña actualizada correctamente. Todas las sesiones han sido cerradas.')
                    return redirect('login')
                except Usuario.DoesNotExist:
                    messages.error(request, 'No se encontró el usuario para actualizar la contraseña.')
            else:
                messages.error(request, 'No se encontró el correo del usuario en la sesión.')
    # Si el usuario navega manualmente al login, limpiar mensajes
    if request.GET.get('volver_login') == '1':
        storage = get_messages(request)
        for _ in storage:
            pass
        return redirect('login')
    return render(request, 'nueva_contraseña.html')

# Vistas de  membresias
def membresias_view(request):
    """Vista para administrar membresías"""
    membresias = rm.obtenerMembresias()
    
    context = {
        'membresias': membresias
    }
    
    return render(request, 'membresias.html', context)

def obtener_membresia(request):
    """Obtener datos de una membresía para editar"""
    if request.method == 'GET':
        membresia_id = request.GET.get('id')
        
        try:
            membresia = rm.obtenerMembresias().objects.get(id_membresia=membresia_id)
            
            data = {
                'success': True,
                'membresia': {
                    'id_membresia': membresia.id_membresia,
                    'nombreMembresia': membresia.nombreMembresia,
                    'duracionDias': membresia.duracionDias,
                    'precio': float(membresia.precio) if membresia.precio else 0
                }
            }
            
            return JsonResponse(data)
        except rm.obtenerMembresias().DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Membresía no encontrada'})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def guardar_membresia(request):
    """Guardar o actualizar una membresía"""
    if request.method == 'POST':
        membresia_id = request.POST.get('membresia_id')
        nombre = request.POST.get('nombreMembresia')
        duracion = request.POST.get('duracionDias')
        precio = request.POST.get('precio')
        modo_edicion = request.POST.get('modo_edicion') == '1'
        
        if membresia_id:  # Editar membresía existente
            membresia = get_object_or_404(rm.obtenerMembresias(), id_membresia=membresia_id)
            
            # Si estamos en modo edición, solo actualizamos el precio
            if modo_edicion:
                membresia.precio = float(precio)
            else:
                # Si no estamos en modo edición, actualizamos todos los campos
                membresia.nombreMembresia = nombre
                membresia.duracionDias = int(duracion)
                membresia.precio = float(precio)
                
            membresia.save()
            
            messages.success(request, f'Membresía "{membresia.nombreMembresia}" actualizada correctamente')
        else:  # Crear nueva membresía
            membresia = rm.obtenerMembresias().objects.create(
                nombreMembresia=nombre,
                duracionDias=int(duracion),
                precio=float(precio)
            )
            
            messages.success(request, f'Membresía "{nombre}" creada correctamente')
        
        return redirect('membresias')
    
    return redirect('membresias')

def eliminar_membresia(request):
    """Eliminar una membresía"""
    if request.method == 'POST':
        membresia_id = request.POST.get('membresia_id')
        
        # Verificar que el ID no esté vacío
        if not membresia_id:
            messages.error(request, 'Error: No se ha especificado el ID de la membresía a eliminar')
            return redirect('membresias')
        
        try:
            # Convertir explícitamente a entero
            membresia_id = int(membresia_id)
            membresia = rm.obtenerMembresias().objects.get(id_membresia=membresia_id)
            nombre = membresia.nombreMembresia
            membresia.delete()
            
            messages.success(request, f'Membresía "{nombre}" eliminada correctamente')
        except ValueError:
            messages.error(request, 'Error: El ID de la membresía no es válido')
        except rm.obtenerMembresias().DoesNotExist:
            messages.error(request, 'Membresía no encontrada')
        
        return redirect('membresias')
    
    return redirect('membresias')

    #vista de maquinas
def maquinas_view(request):
    # Obtener todas las máquinas
    maquinas = Maquina.objects.all()
    
    # Convertir las máquinas a formato JSON para usar en JavaScript
    maquinas_json = json.dumps([{
        'id_maquina': maquina.id_maquina,
        'nombre': maquina.nombre,
        'cantidad': maquina.cantidad,
        'estado': maquina.estado,
        'descripcion': maquina.descripcion,
        'razon_inactividad': maquina.razon_inactividad,
        'fecha_inactividad': maquina.fecha_inactividad.strftime('%Y-%m-%d') if maquina.fecha_inactividad else None,
        'notas_inactividad': maquina.notas_inactividad,
        'fecha_estimada_reparacion': maquina.fecha_estimada_reparacion.strftime('%Y-%m-%d') if maquina.fecha_estimada_reparacion else None,
        'imagen_url': request.build_absolute_uri(maquina.imagen.url) if maquina.imagen else None
    } for maquina in maquinas])
    
    # Obtener máquinas en reparación o mal estado
    maquinas_inactivas = Maquina.objects.filter(estado='inactiva')
    
    context = {
        'maquinas': maquinas,
        'maquinas_json': maquinas_json,
        'maquinas_inactivas': maquinas_inactivas
    }
    
    return render(request, 'maquinas.html', context)

def editar_maquina(request):
    if request.method == 'POST':
        maquina_id = request.POST.get('maquina_id')
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        estado = request.POST.get('estado')
        descripcion = request.POST.get('descripcion')
        
        # Buscar la máquina por ID
        maquina = get_object_or_404(Maquina, id_maquina=maquina_id)
        
        # Actualizar los campos básicos
        maquina.nombre = nombre
        maquina.cantidad = int(cantidad)
        maquina.descripcion = descripcion
        
        # Manejar el cambio de estado
        estado_anterior = maquina.estado
        maquina.estado = estado
        
        # Si la máquina pasa de activa a inactiva, registrar información adicional
        if estado_anterior == 'activa' and estado == 'inactiva':
            razon_inactividad = request.POST.get('razon_inactividad')
            notas_inactividad = request.POST.get('notas_inactividad')
            fecha_estimada = request.POST.get('fecha_estimada_reparacion')
            
            maquina.razon_inactividad = razon_inactividad
            maquina.notas_inactividad = notas_inactividad
            maquina.fecha_inactividad = date.today()
            
            if fecha_estimada:
                maquina.fecha_estimada_reparacion = fecha_estimada
        
        # Si la máquina pasa de inactiva a activa, resetear los campos de inactividad
        elif estado_anterior == 'inactiva' and estado == 'activa':
            maquina.razon_inactividad = 'no_aplica'
            maquina.notas_inactividad = None
            maquina.fecha_inactividad = None
            maquina.fecha_estimada_reparacion = None
        
        # Manejar la imagen si se proporciona una nueva
        if 'imagen' in request.FILES:
            maquina.imagen = request.FILES['imagen']
        
        # Guardar los cambios
        maquina.save()
        
        messages.success(request, f'Máquina "{nombre}" actualizada correctamente')
        return redirect('maquinas')
    
    # Si no es POST, redirigir a la página de máquinas
    return redirect('maquinas')

def agregar_maquina(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        estado = request.POST.get('estado')
        descripcion = request.POST.get('descripcion')
        
        # Crear nueva máquina
        maquina = Maquina(
            nombre=nombre,
            cantidad=int(cantidad),
            estado=estado,
            descripcion=descripcion
        )
        
        # Si la máquina es inactiva, registrar información adicional
        if estado == 'inactiva':
            razon_inactividad = request.POST.get('razon_inactividad')
            notas_inactividad = request.POST.get('notas_inactividad')
            fecha_estimada = request.POST.get('fecha_estimada_reparacion')
            
            maquina.razon_inactividad = razon_inactividad
            maquina.notas_inactividad = notas_inactividad
            maquina.fecha_inactividad = date.today()
            
            if fecha_estimada:
                maquina.fecha_estimada_reparacion = fecha_estimada
        
        # Manejar la imagen si se proporciona
        if 'imagen' in request.FILES:
            maquina.imagen = request.FILES['imagen']
        
        # Guardar la máquina
        maquina.save()
        
        messages.success(request, f'Máquina "{nombre}" agregada correctamente')
        return redirect('maquinas')
    
    # Si es GET, mostrar el formulario para agregar
    return render(request, 'agregar_maquina.html')

def maquinas_inactivas_view(request):
    # Obtener máquinas inactivas
    maquinas_inactivas = Maquina.objects.filter(estado='inactiva')
    
    context = {
        'maquinas_inactivas': maquinas_inactivas
    }
    
    return render(request, 'maquinas_inactivas.html', context)

def dashboard_empleado(request):
    # Obtener el parámetro de días para filtrar
    days_filter = request.GET.get('days', '7')
    try:
        days = int(days_filter)
    except ValueError:
        days = 7  # Valor por defecto
    
    # Fecha actual
    today = timezone.now().date()
    
    # Obtener todas las membresías
    all_memberships = MembresiaCliente.objects.select_related('cliente', 'membresia').all()
    
    # Obtener membresías que vencen en los próximos X días
    expiring_date = today + timedelta(days=days)
    memberships_expiring = []
    
    for membership in all_memberships:
        if membership.fecha_fin and today <= membership.fecha_fin <= expiring_date:
            # Calcular días restantes
            days_left = (membership.fecha_fin - today).days
            membership.days_left = days_left
            memberships_expiring.append(membership)
    
    # Ordenar por fecha de vencimiento (más cercana primero)
    memberships_expiring.sort(key=lambda x: x.fecha_fin)
    
    # Obtener membresías vencidas
    expired_memberships_list = []
    
    for membership in all_memberships:
        if membership.fecha_fin and membership.fecha_fin < today:
            # Calcular días vencidos
            days_expired = (today - membership.fecha_fin).days
            membership.days_expired = days_expired
            expired_memberships_list.append(membership)
    
    # Ordenar por fecha de vencimiento (más reciente primero)
    expired_memberships_list.sort(key=lambda x: x.fecha_fin, reverse=True)
    
    # Contar membresías por tipo
    diaria_count = MembresiaCliente.objects.filter(
        membresia__nombreMembresia='Diaria',
        fecha_fin__gte=today
    ).count()
    
    semanal_count = MembresiaCliente.objects.filter(
        membresia__nombreMembresia='Semanal',
        fecha_fin__gte=today
    ).count()
    
    quincenal_count = MembresiaCliente.objects.filter(
        membresia__nombreMembresia='Quincenal',
        fecha_fin__gte=today
    ).count()
    
    mensual_count = MembresiaCliente.objects.filter(
        membresia__nombreMembresia='Mensual',
        fecha_fin__gte=today
    ).count()
    
    # Estadísticas generales
    total_clients = Cliente.objects.count()
    active_memberships = MembresiaCliente.objects.filter(fecha_fin__gte=today).count()
    expired_memberships = MembresiaCliente.objects.filter(fecha_fin__lt=today).count()
    
    # Obtener todos los tipos de membresía para el formulario de renovación
    tipos_membresia = TipoMembresia.objects.all()
    
    context = {
        'total_clients': total_clients,
        'active_memberships': active_memberships,
        'expired_memberships': expired_memberships,
        'memberships_expiring': memberships_expiring,
        'memberships_expiring_count': len(memberships_expiring),
        'expired_memberships_list': expired_memberships_list,
        'tipos_membresia': tipos_membresia,
        'diaria_count': diaria_count,
        'semanal_count': semanal_count,
        'quincenal_count': quincenal_count,
        'mensual_count': mensual_count,
        'days_filter': days,
    }
    
    return render(request, 'dashboard_empleado.html', context)

@csrf_exempt
def realizar_pago_api(request):
    if request.method == 'POST':
        from django.http import JsonResponse
        try:
            data = json.loads(request.body)
            cliente_id = data.get('cliente_id')
            productos = data.get('productos', [])
            membresias = data.get('membresias', [])
            descuento = data.get('descuento', 0)
            total = data.get('total', 0)
            if not cliente_id or (not productos and not membresias):
                return JsonResponse({'success': False, 'error': 'Cliente y productos o membresías son requeridos.'}, status=400)
            # Obtener cliente
            cliente = rc.obtenerClientePorId(cliente_id)
            if not cliente:
                return JsonResponse({'success': False, 'error': 'Cliente no encontrado.'}, status=404)
            fecha_actual = date.today().isoformat()
            pago_realizado = False
            # Procesar productos si existen
            if productos:
                productos_para_pago = []
                for prod in productos:
                    if prod.get('type') != 'product':
                        continue  # Solo productos, no membresías
                    producto_obj = rp.obtenerProductoPorId(prod['id']) if hasattr(rp, 'obtenerProductoPorId') else None
                    if not producto_obj:
                        return JsonResponse({'success': False, 'error': f"Producto con id {prod['id']} no encontrado."}, status=400)
                    productos_para_pago.append({'producto': producto_obj, 'cantidad': prod['quantity']})
                if productos_para_pago:
                    # Registrar el pago principal (ahora con fecha actual)
                    valido_pago, mensaje_pago = spg.registrarPago(
                        tipo="Producto",
                        fecha=fecha_actual,
                        cliente=cliente,
                        productos=productos_para_pago
                    )
                    if not valido_pago:
                        return JsonResponse({'success': False, 'error': mensaje_pago}, status=400)
                    # Obtener el último pago registrado para el cliente
                    pago = rpa.obtenerUltimoPagoPorCliente(cliente)
                    if not pago:
                        return JsonResponse({'success': False, 'error': 'No se pudo registrar el pago.'}, status=400)
                    # Registrar productos asociados al pago
                    from main.servicio import servicioPagoProducto as spp
                    for prod in productos_para_pago:
                        spp.registrarPagoProducto(
                            pago=pago,
                            producto=prod['producto'],
                            fecha_pago=fecha_actual,
                            cantidad=prod['cantidad']
                        )
                        # Restar stock del producto vendido
                        prod_obj = prod['producto']
                        prod_obj.existencia -= prod['cantidad']
                        prod_obj.save()
                    pago_realizado = True
            # Procesar membresías si existen
            if membresias:
                from main.servicio import servicioPagos as spg
                for memb in membresias:
                    # Aquí deberías adaptar según tu lógica de membresía
                    valido_pago, mensaje_pago = spg.registrarPagoMembresia(
                        fecha=fecha_actual,
                        cliente=cliente,
                        membresia_id=memb['id'],
                        cantidad=memb.get('quantity', 1)
                    )
                    if not valido_pago:
                        return JsonResponse({'success': False, 'error': mensaje_pago}, status=400)
                    pago_realizado = True
            if not pago_realizado:
                return JsonResponse({'success': False, 'error': 'No se pudo registrar el pago.'}, status=400)
            # Registrar descuento si aplica (solo si hubo pago)
            if descuento and float(descuento) > 0:
                descuento_obj = rpd.obtenerDescuentoPorMonto(float(descuento)) if hasattr(rpd, 'obtenerDescuentoPorMonto') else None
                if descuento_obj:
                    spd.registrarPagoDescuentos(pago, descuento_obj)
            productos_actualizados = sp.prepararVistaProductos()
            # Si la petición es AJAX (fetch), responder con JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': '¡Compra realizada con éxito!', 'productos': productos_actualizados})
            # Si es POST normal, usar messages y redirigir
            messages.success(request, '¡Compra realizada con éxito!')
            return redirect('pagos')
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from main.repositorio import repositorioMembresia as rm

@csrf_exempt
def api_tipo_membresias(request):
    if request.method == 'GET':
        membresias = rm.obtenerMembresias()
        data = []
        for m in membresias:
            data.append({
                'id_membresia': m.id_membresia,
                'nombreMembresia': m.nombreMembresia,
                'precio': m.precio,
                'duracionDias': m.duracionDias,
                'features': [],  # Puedes agregar lógica para features si existe
                'imagen': getattr(m, 'imagen', None)  # Si tienes campo imagen
            })
        return JsonResponse({'membresias': data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

    """Verifica si el usuario es administrador"""
    return user.is_authenticated and user.is_staff

def empleados_view(request):
    """Lista de empleados"""
    empleados = Empleado.objects.all().order_by('nombre_empleado')
    
    # Filtrar por rol si se especifica
    rol_filtro = request.GET.get('rol', '')
    if rol_filtro:
        empleados = empleados.filter(rol=rol_filtro)
    
    # Filtrar por estado si se especifica
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        activo = estado_filtro == 'activo'
        empleados = empleados.filter(activo=activo)
    
    # Buscar por nombre si se especifica
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        empleados = empleados.filter(nombre_empleado__icontains=busqueda)
    
    context = {
        'empleados': empleados,
        'rol_filtro': rol_filtro,
        'estado_filtro': estado_filtro,
        'busqueda': busqueda,
    }
    
    return render(request, 'empleados.html', context)





