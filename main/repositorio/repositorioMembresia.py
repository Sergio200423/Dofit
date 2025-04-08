from main.models import Membresia

def obtenerMembresias():
    """
    Obtiene todas las membresías de la base de datos.
    :return: QuerySet de objetos Membresia
    """
    return Membresia.objects.all()

def obtenerMembresiaPorNombre(nombreMembresia):
    """
    Obtiene una membresía específica por su nombre.
    :return: QuerySet de objetos Membresia
    """
    return Membresia.objects.filter(nombre=nombreMembresia).first()