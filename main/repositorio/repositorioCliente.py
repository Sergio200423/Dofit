from main.models import Cliente
from main.models import Membresia

def crearCiente(nombre, fecha_nacimiento, sexo, fecha_inicio, membresia):
    """
    Crea un nuevo cliente en la base de datos.
    :param nombre: Nombre del cliente
    :param fecha_nacimiento: Fecha de nacimiento del cliente
    :param sexo: Sexo del cliente
    :param fecha_inicio: Fecha de inicio de membresía
    :param membresia: Tipo de membresía
    :return: Objeto Cliente creado
    """
    cliente = Cliente.objects.create(
        nombre_cliente=nombre, 
        fecha_nacimiento=fecha_nacimiento, 
        sexo=sexo, fecha_inicio=fecha_inicio,
        membresia=membresia)
    
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

def UnirClienteMembresia():
    """
    Asocia un cliente con una membresía.
    :param cliente: Objeto Cliente
    :param membresia: Objeto Membresia
    :return: Objeto Cliente actualizado
    """
    return Cliente.objects.select_related('membresia').all()