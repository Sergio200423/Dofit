from datetime import datetime
from clientes import repositorioCliente as rc
from django.utils.timezone import now

def validarFechaNacimiento(fecha_nacimiento):
    """
    Valida si la fecha de nacimiento es mayor a 14 años desde la fecha actual.
    :param fecha_nacimiento: Fecha de nacimiento en formato 'YYYY-MM-DD'
    :return: True si es mayor de edad, False si no lo es
    """
    try: 
        fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        edad = (datetime.now().date() - fecha_nacimiento_dt).days // 365
        if edad < 14:
            return False, 'La edad mínima es 14 años.'
        return True, ''
    except ValueError:
        return False, 'Formato de fecha inválido. Debe ser YYYY-MM-DD.'
    
def validarClientesRepetidos(nombre, fecha_nacimiento):
    """
    Valida si el cliente ya existe en la base de datos.
    """
    # Obtener la lista de clientes existentes
    clientes = rc.obtenerClientes()
    for cliente in clientes:
        if cliente.nombre_cliente == nombre and cliente.fecha_nacimiento == fecha_nacimiento:
            return False, 'El cliente ya existe.'
    return True, ''

def validarCamposVacios(nombre, fecha_nacimiento, sexo, fecha_registro):
    """
    Valida si los campos de entrada están vacíos.
    :param nombre: Nombre del cliente
    :param fecha_nacimiento: Fecha de nacimiento del cliente
    :param sexo: Sexo del cliente
    :param fecha_inicio: Fecha de inicio de membresía
    :return: True si todos los campos están completos, False si alguno está vacío
    """
    if not nombre or not fecha_nacimiento or not sexo or not fecha_registro:
        return False, 'Todos los campos son obligatorios.'
    return True, ''

def validarEstudiante(estudiante):
    """
    Valida si el cliente tiene el campo estudiante definido.
    :param estudiante: Valor del campo estudiante (True, False o None)
    :return: (bool, str) -> False si el campo es None, True si es válido
    """
    if estudiante is None:
        return False, "El cliente no tiene definido si es estudiante."
    return True, ""

def registrarClientes(nombre, fecha_nacimiento, sexo, fecha_registro, carnet_estudiante=None):
    """
    Registra un cliente después de validar los datos.
    :param nombre: Nombre del cliente
    :param fecha_nacimiento: Fecha de nacimiento del cliente
    :param sexo: Sexo del cliente
    :param fecha_inicio: Fecha de inicio de membresía
    :param carnet_estudiante: Carnet de estudiante (opcional)
    :return: (bool, str) -> True si el cliente se creó correctamente, False y un mensaje de error en caso contrario
    """
    # Validar campos vacíos
    valido, mensaje = validarCamposVacios(nombre, fecha_nacimiento, sexo, fecha_registro)
    if not valido:
        return False, mensaje

    # Validar fecha de nacimiento
    valido, mensaje = validarFechaNacimiento(fecha_nacimiento)
    if not valido:
        return False, mensaje

    # Validar si el cliente ya existe
    valido, mensaje = validarClientesRepetidos(nombre, fecha_nacimiento)
    if not valido:
        return False, mensaje

    # Crear el cliente en la base de datos
    try:
        cliente = rc.crearCliente(nombre, fecha_nacimiento, sexo, fecha_registro, carnet_estudiante)
        return True, f"Cliente '{cliente.nombre_cliente}' registrado exitosamente."
    except Exception as e:
        return False, f"Error al registrar el cliente: {str(e)}"
    
def prepararVistaClientesConMembresiaActiva():
    """
    Prepara los datos de clientes con membresías activas para la vista.
    """
    clientes = rc.obtenerClientesConMembresiaActiva()
    clientes_vista = []

    for cliente in clientes:
        membresia_activa = cliente.membresias_cliente.filter(fecha_fin__gte=now().date()).first()

        clientes_vista.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'sexo': cliente.sexo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'carnet_estudiante': cliente.estudiante,
            'membresia': {
                'nombreMembresia': membresia_activa.membresia.nombreMembresia if membresia_activa else None,
                'estado': 'activo' if membresia_activa else 'sin membresía',
                'fecha_inicio': membresia_activa.fecha_inicio if membresia_activa else None,
                'fecha_fin': membresia_activa.fecha_fin if membresia_activa else None
            }
        })

    return clientes_vista

def prepararVistaClientesConMembresiaInactiva():
    """
    Prepara los datos de clientes con membresías inactivas para la vista.
    """
    clientes = rc.obtenerClientesConMembresiaInactiva()
    clientes_vista = []

    for cliente in clientes:
        # Obtener la primera membresía inactiva del cliente
        membresia_inactiva = cliente.membresias_cliente.filter(fecha_fin__lt=now().date()).first()

        # Agregar los datos del cliente a la lista
        clientes_vista.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'sexo': cliente.sexo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'carnet_estudiante': cliente.estudiante,
            'membresia': {
                'nombreMembresia': membresia_inactiva.membresia.nombreMembresia if membresia_inactiva else None,
                'estado': 'inactivo' if membresia_inactiva else 'sin membresía',
                'fecha_inicio': membresia_inactiva.fecha_inicio if membresia_inactiva else None,
                'fecha_fin': membresia_inactiva.fecha_fin if membresia_inactiva else None
            }
        })

    return clientes_vista

def prepararVistaTodosLosClientes():
    """
    Prepara los datos de todos los clientes, sin importar si tienen membresías activas o inactivas.
    """
    clientes = rc.obtenerTodosLosClientes()
    clientes_vista = []

    for cliente in clientes:
        # Obtener todas las membresías del cliente
        membresias = cliente.membresias_cliente.all()

        # Determinar la membresía activa e inactiva
        membresia_activa = next(
            (m for m in membresias if m.fecha_fin and m.fecha_fin >= now().date()), None
        )


        # Asignar estado y membresía
        if membresia_activa:
            estado = 'activo'
            membresia = membresia_activa
        else:
            estado = 'inactivo'
            membresia = None

        # Agregar cliente a la lista de vista
        clientes_vista.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'sexo': cliente.sexo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'carnet_estudiante': cliente.estudiante,
            'membresia': {
                'nombreMembresia': membresia.membresia.nombreMembresia if membresia else 'Inactiva',
                'estado': estado,
                'fecha_inicio': membresia.fecha_inicio.strftime('%Y-%m-%d') if membresia and membresia.fecha_inicio else None,
                'fecha_fin': membresia.fecha_fin.strftime('%Y-%m-%d') if membresia and membresia.fecha_fin else None
            }
        })

    return clientes_vista

def prepararVistaClientesConMembresiaDiaria():
    """
    Prepara los datos de clientes con membresías diarias para la vista.
    """
    clientes = rc.obtenerClientesConMembresiaDiaria()
    clientes_vista = []

    for cliente in clientes:
        membresia = cliente.membresias_cliente.filter(membresia__nombreMembresia='Diaria').first()

        if membresia and membresia.fecha_fin >= now().date():
            estado = 'activo'
        elif membresia:
            estado = 'inactivo'
        else:
            estado = 'sin membresía'

        clientes_vista.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'sexo': cliente.sexo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'carnet_estudiante': cliente.estudiante,
            'membresia': {
                'nombreMembresia': membresia.membresia.nombreMembresia if membresia else None,
                'estado': estado,
                'fecha_inicio': membresia.fecha_inicio if membresia else None,
                'fecha_fin': membresia.fecha_fin if membresia else None
            }
        })

    return clientes_vista

def prepararVistaClientesConMembresiaSemanal():
    """
    Prepara los datos de clientes con membresías semanales para la vista.
    """
    clientes = rc.obtenerClientesConMembresiaSemanal()
    clientes_vista = []

    for cliente in clientes:
        # Obtener la membresía semanal del cliente
        membresia = cliente.membresias_cliente.filter(membresia__nombreMembresia='Semanal').first()

        # Determinar el estado de la membresía
        if membresia and membresia.fecha_fin >= now().date():
            estado = 'activo'
        elif membresia:
            estado = 'inactivo'
        else:
            estado = 'sin membresía'

        # Agregar los datos del cliente a la lista
        clientes_vista.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'sexo': cliente.sexo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'carnet_estudiante': cliente.estudiante,
            'membresia': {
                'nombreMembresia': membresia.membresia.nombreMembresia if membresia else None,
                'estado': estado,
                'fecha_inicio': membresia.fecha_inicio if membresia else None,
                'fecha_fin': membresia.fecha_fin if membresia else None
            } if membresia else None
        })

    return clientes_vista
    return clientes_vista

def prepararVistaClientesConMembresiaQuincenal():
    """
    Prepara los datos de clientes con membresías quincenales para la vista.
    """
    clientes = rc.obtenerClientesConMembresiaQuincenal()
    clientes_vista = []

    for cliente in clientes:
        # Asegúrate de que el filtro coincida con el valor exacto en la base de datos
        membresia = cliente.membresias_cliente.filter(membresia__nombreMembresia='Quincenal').first()

        # Determinar el estado de la membresía
        if membresia and membresia.fecha_fin >= now().date():
            estado = 'activo'
        elif membresia:
            estado = 'inactivo'
        else:
            estado = 'sin membresía'

        # Agregar los datos del cliente a la lista
        clientes_vista.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'sexo': cliente.sexo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'carnet_estudiante': cliente.estudiante,
            'membresia': {
                'nombreMembresia': membresia.membresia.nombreMembresia if membresia else None,
                'estado': estado,
                'fecha_inicio': membresia.fecha_inicio if membresia else None,
                'fecha_fin': membresia.fecha_fin if membresia else None
            } if membresia else None
        })

    return clientes_vista

def prepararVistaClientesConMembresiaMensual():
    """
    Prepara los datos de clientes con membresías mensuales para la vista.
    """
    clientes = rc.obtenerClientesConMembresiaMensual()
    clientes_vista = []

    for cliente in clientes:
        membresia = cliente.membresias_cliente.filter(membresia__nombreMembresia='Mensual').first()

        # Determinar el estado de la membresía
        if membresia and membresia.fecha_fin >= now().date():
            estado = 'activo'
        elif membresia:
            estado = 'inactivo'
        else:
            estado = 'sin membresía'

        clientes_vista.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'sexo': cliente.sexo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'carnet_estudiante': cliente.estudiante,
            'membresia': {
                'nombreMembresia': membresia.membresia.nombreMembresia if membresia else None,
                'estado': estado,
                'fecha_inicio': membresia.fecha_inicio if membresia else None,
                'fecha_fin': membresia.fecha_fin if membresia else None
            } if membresia else None
        })

    return clientes_vista

from django.db.models import OuterRef, Subquery
from main.models import MembresiaCliente, Cliente
from django.utils import timezone

def filtrar_clientes(nombre=None, sexo=None, membresias=None, estado=None):
    try:
        qs = Cliente.objects.all()
        if nombre:
            qs = qs.filter(nombre_cliente__icontains=nombre)
        if sexo:
            qs = qs.filter(sexo__in=sexo)

        membresia_filter = {}
        if membresias:
            membresia_filter['membresia__nombreMembresia__in'] = membresias
        # No filtrar por estado aquí, lo haremos en Python

        membresia_subquery = MembresiaCliente.objects.filter(
            cliente=OuterRef('pk'),
            **membresia_filter
        ).order_by('-fecha_fin')

        qs = qs.annotate(
            membresia_id=Subquery(membresia_subquery.values('id_membresia_cliente')[:1])
        )

        membresias_dict = {
            m.id_membresia_cliente: m for m in MembresiaCliente.objects.select_related('membresia')
        }
        clientes_vista = []
        for cliente in qs:
            membresia = membresias_dict.get(cliente.membresia_id)
            if membresia:
                estado_membresia = 'activo' if membresia.fecha_fin and membresia.fecha_fin > timezone.now().date() else 'inactivo'
            else:
                estado_membresia = 'sin membresía'
            # Solo filtra si la lista estado NO está vacía
            if estado and len(estado) > 0 and estado_membresia not in estado:
                continue

            clientes_vista.append({
                'id_cliente': cliente.id_cliente,
                'nombre_cliente': cliente.nombre_cliente,
                'sexo': cliente.sexo,
                'fecha_nacimiento': cliente.fecha_nacimiento,
                'carnet_estudiante': cliente.estudiante,
                'membresia': {
                    'nombreMembresia': membresia.membresia.nombreMembresia if membresia else None,
                    'estado': estado_membresia,
                    'fecha_inicio': membresia.fecha_inicio if membresia else None,
                    'fecha_fin': membresia.fecha_fin if membresia else None
                } if membresia else None
            })
        return clientes_vista
    except Exception as e:
        print("Error en filtrar_clientes:", e)
        raise
