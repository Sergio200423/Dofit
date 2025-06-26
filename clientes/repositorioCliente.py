from django.utils.timezone import now
from main.models import Cliente, MembresiaCliente  # Importa MembresiaCliente
from django.db.models.functions import Lower
from django.db.models import Prefetch
from datetime import datetime

def crearCliente(nombre, fecha_nacimiento, sexo, fecha_registro, carnet_estudiante=None):
    """
    Crea un nuevo cliente en la base de datos.
    :param nombre: Nombre del cliente
    :param fecha_nacimiento: Fecha de nacimiento del cliente
    :param sexo: Sexo del cliente
    :param fecha_registro: Fecha de registro del cliente
    :param carnet_estudiante: Carnet de estudiante (opcional)
    :return: Objeto Cliente creado
    """
    cliente = Cliente.objects.create(
        nombre_cliente=nombre,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo,
        fecha_registro=fecha_registro,
        estudiante=carnet_estudiante  # Agregar el carnet de estudiante
    )
    return cliente

def obtenerOpcionesSexo():
    """
    Obtiene las opciones de sexo definidas en el modelo Cliente.
    :return: Lista de tuplas con las opciones de sexo
    """
    return Cliente._meta.get_field('sexo').choices

def obtenerTodosLosClientesConMembresia():
    """
    Obtiene todos los clientes que tienen al menos una membresía.
    :return: QuerySet de objetos Cliente con membresías
    """
    membresias_prefetch = Prefetch(
        'membresias_cliente',
        queryset=MembresiaCliente.objects.select_related('membresia').order_by('-fecha_fin'),
        to_attr='membresias_cliente_prefetch'
    )
    return Cliente.objects.all().prefetch_related(membresias_prefetch)

def obtenerClientes():
    """
    Obtiene todos los clientes de la base de datos.
    :return: QuerySet de objetos Cliente
    """
    return Cliente.objects.all()

def obtenerClientePorNombre(nombre_cliente):
    """
    Obtiene un cliente específico por su nombre.
    :param nombre_cliente: Nombre del cliente
    :return: Objeto Cliente o None si no se encuentra
    """
    return Cliente.objects.filter(nombre_cliente=nombre_cliente).first()

from django.db.models.functions import Lower

def obtenerClientePorId(cliente_id):
    """
    Obtiene un cliente por su ID.
    """
    try:
        return Cliente.objects.get(id_cliente=cliente_id)
    except Cliente.DoesNotExist:
        return None

def actualizarCliente(cliente_id, nombre, sexo, fecha_nacimiento):
    """
    Actualiza los datos de un cliente.
    """
    cliente = obtenerClientePorId(cliente_id)
    if not cliente:
        return False, "No se encontró el cliente."

    # Validar datos
    if not nombre or not isinstance(nombre, str):
        return False, "El nombre proporcionado no es válido."
    if sexo not in [opcion[0] for opcion in Cliente._meta.get_field('sexo').choices]:
        return False, "El sexo proporcionado no es válido."
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
    except ValueError:
        return False, "La fecha de nacimiento no tiene un formato válido (YYYY-MM-DD)."

    # Actualizar campos
    cliente.nombre_cliente = nombre
    cliente.sexo = sexo
    cliente.fecha_nacimiento = fecha_nacimiento

    # Guardar cambios
    try:
        cliente.save()
        return True, "Cliente actualizado correctamente."
    except Exception as e:
        return False, f"Error al guardar los cambios: {str(e)}"


def obtenerClientesConMembresiaActiva():
    """
    Obtiene todos los clientes con membresías activas, ordenados por nombre de la A a la Z.
    Una membresía activa es aquella cuya fecha_fin es mayor o igual a la fecha actual.
    """
    return Cliente.objects.prefetch_related(
        'membresias_cliente__membresia'  # Relación con MembresiaCliente y Membresia
    ).filter(
        membresias_cliente__fecha_fin__gte=now().date()  # Filtrar solo membresías activas
    ).annotate(
        nombre_cliente_lower=Lower('nombre_cliente')  # Ordenar por nombre en minúsculas
    ).order_by('nombre_cliente_lower')

def obtenerClientesConMembresiaInactiva():
    """
    Obtiene todos los clientes con membresías inactivas, ordenados por nombre de la A a la Z.
    Una membresía inactiva es aquella cuya fecha_fin es menor a la fecha actual.
    """
    return Cliente.objects.prefetch_related(
        'membresias_cliente__membresia'  # Relación con MembresiaCliente y Membresia
    ).filter(
        membresias_cliente__fecha_fin__lt=now().date()  # Filtrar solo membresías inactivas
    ).annotate(
        nombre_cliente_lower=Lower('nombre_cliente')  # Ordenar por nombre en minúsculas
    ).order_by('nombre_cliente_lower')

def obtenerTodosLosClientes():
    """
    Obtiene todos los clientes, sin importar si tienen membresías activas o inactivas.
    """
    return Cliente.objects.all()

def obtenerClientesConMembresiaDiaria():
    """
    Obtiene todos los clientes con membresías diarias.
    """
    return Cliente.objects.prefetch_related(
        'membresias_cliente__membresia'  # Relación con MembresiaCliente y TipoMembresia
    ).filter(
        membresias_cliente__membresia__nombreMembresia='Diaria'  # Filtrar por nombre de membresía
    ).annotate(
        nombre_cliente_lower=Lower('nombre_cliente')  # Ordenar por nombre en minúsculas
    ).order_by('nombre_cliente_lower')



def obtenerClientesConMembresiaSemanal():
    """
    Obtiene todos los clientes con membresías semanales.
    """
    return Cliente.objects.prefetch_related(
        'membresias_cliente__membresia'  # Relación con MembresiaCliente y TipoMembresia
    ).filter(
        membresias_cliente__membresia__nombreMembresia='Semanal'  # Filtrar por nombre de membresía
    ).annotate(
        nombre_cliente_lower=Lower('nombre_cliente')  # Ordenar por nombre en minúsculas
    ).order_by('nombre_cliente_lower')


def obtenerClientesConMembresiaQuincenal():
    """
    Obtiene todos los clientes con membresías quincenales.
    """
    return Cliente.objects.prefetch_related(
        'membresias_cliente__membresia'
    ).filter(
        membresias_cliente__membresia__nombreMembresia='Quincenal'  # Filtrar por nombre de membresía
    ).annotate(
        nombre_cliente_lower=Lower('nombre_cliente')
    ).order_by('nombre_cliente_lower')


def obtenerClientesConMembresiaMensual():
    """
    Obtiene todos los clientes con membresías mensuales.
    """
    return Cliente.objects.prefetch_related(
        'membresias_cliente__membresia'
    ).filter(
        membresias_cliente__membresia__nombreMembresia='Mensual'  # Filtrar por nombre de membresía
    ).annotate(
        nombre_cliente_lower=Lower('nombre_cliente')
    ).order_by('nombre_cliente_lower')