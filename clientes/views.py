#Importaciones de Django
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
import json

#Repositorios clientes
from clientes import repositorioCliente as rc
from clientes import repositorioMembresiaCliente as rmc

#Servicios clientes
from clientes import servicioClientes as sc

#Repositorios membresias
from membresias import repositorioMembresia as rm

#Repositorios pagos
from pagos import repositorioPago as rp
from pagos import repositorioPagoDescuento as rpd

#Servicios pago
from pagos import servicioPagos as sp
from pagos import servicioPagoDescuento as spd
from clientes.utils.contador import contar_total_clientes, contar_membresias_activas, contar_membresias_por_vencer, contar_membresias_expiradas, contar_membresias_diarias_activas, contar_membresias_semanales_activas, contar_membresias_quincenales_activas, contar_membresias_mensuales_activas

# Create your views here.
def index(request):
    """Cargamos la vista de inicio de la aplicacion.
    """
    total_clients = contar_total_clientes()
    membresias_activas = contar_membresias_activas()
    membresias_por_vencer = contar_membresias_por_vencer()
    membresias_expiradas = contar_membresias_expiradas()
    lista_membresias_por_vencer = rmc.RepositorioMembresiaCliente.obtener_membresias_por_vencer()
    lista_membresias_expiradas = rmc.RepositorioMembresiaCliente.obtener_membresias_expiradas()
    contador_diaria = contar_membresias_diarias_activas()
    contador_semanal = contar_membresias_semanales_activas()
    contador_semanal = contar_membresias_quincenales_activas()
    contador_mensual = contar_membresias_mensuales_activas()
    tipos_membresia = rm.obtenerMembresias()
    return render(request, 'clientes/dashboard.html', {
        'total_clients': total_clients,
        'membresias_activas': membresias_activas,
        'membresias_por_vencer': membresias_por_vencer,
        'membresias_expiradas': membresias_expiradas,
        'lista_membresias_por_vencer': lista_membresias_por_vencer,
        'lista_membresias_expiradas': lista_membresias_expiradas,
        'contador_diaria': contador_diaria,
        'contador_semanal': contador_semanal,
        'contador_quincenal': contador_semanal,
        'contador_mensual': contador_mensual,
        'tipos_membresia': tipos_membresia
    })

def clientes(request):
    if request.method == 'GET' and 'cliente_id' in request.GET:
        # Obtener los datos completos de un cliente
        cliente_id = request.GET.get('cliente_id')
        cliente = rc.obtenerClientePorId(cliente_id)
        if not cliente:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)

        # Obtener la membresía asociada al cliente desde la tabla intermedia
        try:
            membresia_cliente = rmc.obtener_membresia_activa(cliente_id)
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
    return render(request, 'clientes/clientes.html', {
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
                resultado_membresia = rmc.crear_membresia_cliente(
                    id_cliente=cliente.id_cliente,
                    id_membresia=membresia.id_membresia,
                    fecha_inicio=fecha_registro
                )

                if not resultado_membresia["success"]:
                    raise Exception(resultado_membresia["error"])

                # Registrar pago
                valido, mensaje_pago = sp.registrarPago(
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
                        pago = rp.obtenerUltimoPagoPorCliente(cliente)
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

def filtrar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

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

            # Si hay filtros, empezar con todos los clientes y filtrar
            clientes = sc.filtrar_clientes(
                nombre=nombre,
                membresias=membresias,
                estado=estado,
                sexo=sexo  
            )

            return JsonResponse({"clientes": clientes})

        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {str(e)}"}, status=500)

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
                membresia_activa = rmc.obtener_membresia_activa(cliente_id)

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

                resultado_membresia = rmc.actualizar_membresia_cliente(
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