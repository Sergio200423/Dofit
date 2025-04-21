from main.models import TipoMembresia

def obtenerMembresias():
    """
    Obtiene todas las membresías de la base de datos.
    :return: QuerySet de objetos Membresia
    """
    return TipoMembresia.objects.all()

def obtenerMembresiaPorNombre(nombreMembresia):
    """
    Obtiene una membresía específica por su nombre.
    :return: QuerySet de objetos Membresia
    """
    return TipoMembresia.objects.filter(nombreMembresia=nombreMembresia).first()