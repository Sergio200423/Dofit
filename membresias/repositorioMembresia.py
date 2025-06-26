from main.models import TipoMembresia

def obtenerMembresias():
    """
    Obtiene todas las membresías de la base de datos.
    :return: QuerySet de objetos Membresia
    """
    return TipoMembresia.objects.all()

def obtenerMembresiaPorId(id_membresia):
    """
    Obtiene una membresía específica por su ID.
    :param id_membresia: ID de la membresía
    :return: Objeto Membresia o lanza DoesNotExist
    """
    return TipoMembresia.objects.get(id_membresia=id_membresia)

def obtenerMembresiaPorNombre(nombreMembresia):
    """
    Obtiene una membresía específica por su nombre.
    :return: QuerySet de objetos Membresia
    """
    return TipoMembresia.objects.filter(nombreMembresia=nombreMembresia).first()