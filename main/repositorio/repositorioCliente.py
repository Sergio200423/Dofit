from django.utils.timezone import now
from main.models import Cliente, MembresiaCliente  # Importa MembresiaCliente

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

def obtenerClientesConMembresiaActiva():
    """
    Obtiene todos los clientes con membresías activas.
    :return: Lista de clientes con información de membresías activas
    """
    clientes = Cliente.objects.prefetch_related(
        'membresias_cliente__membresia'  # Prefetch la relación entre MembresiaCliente y TipoMembresia
    ).all()
    clientes_con_membresia = []

    for cliente in clientes:
        # Filtrar membresías activas (fecha_fin >= hoy)
        membresia_activa = cliente.membresias_cliente.filter(fecha_fin__gte=now().date()).first()
        print(f"Cliente: {cliente.nombre_cliente}, Membresía Activa: {membresia_activa}")  # Depuración

        clientes_con_membresia.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'sexo': cliente.sexo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'carnet_estudiante': cliente.estudiante,  # Agregar el carnet de estudiante
            'membresia_activa': {
                'nombreMembresia': membresia_activa.membresia.nombreMembresia if membresia_activa else None,
                'fecha_inicio': membresia_activa.fecha_inicio if membresia_activa else None,
                'fecha_fin': membresia_activa.fecha_fin if membresia_activa else None,
                'estado': 'activo' if membresia_activa and membresia_activa.fecha_fin >= now().date() else 'inactivo'
            } if membresia_activa else None
        })

    return clientes_con_membresia