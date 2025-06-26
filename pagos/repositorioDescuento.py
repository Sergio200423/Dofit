from main.models import Descuento

def crearDescuento(nombre, monto, descripcion=None):
    """
    Crea un nuevo descuento en la base de datos.
    :param nombre: Nombre del descuento
    :param monto: Monto del descuento
    :param descripcion: Descripción opcional del descuento
    :return: Objeto Descuento creado
    """
    descuento = Descuento.objects.create(
        nombre=nombre,
        monto=monto,
        descripcion=descripcion
    )
    return descuento

def obtenerTodosLosDescuentos():
    """
    Obtiene todos los descuentos de la base de datos.
    :return: QuerySet de objetos Descuento
    """
    return Descuento.objects.all()

def obtenerDescuentoPorNombre(nombre):
    """
    Obtiene un descuento por su nombre.
    :param nombre: Nombre del descuento
    :return: Objeto Descuento si existe, None en caso contrario
    """
    try:
        return Descuento.objects.get(nombre=nombre)
    except Descuento.DoesNotExist:
        return None
    

def obtenerDescuentoPorId(id_descuento):
    """
    Obtiene un descuento específico por su ID.
    :param id_descuento: ID del descuento
    :return: Objeto Descuento o None si no se encuentra
    """
    return Descuento.objects.filter(id_descuento=id_descuento).first()

def actualizarDescuento(id_descuento, nombre=None, monto=None, descripcion=None):
    """
    Actualiza un descuento existente en la base de datos.
    :param id_descuento: ID del descuento a actualizar
    :param nombre: Nuevo nombre del descuento (opcional)
    :param monto: Nuevo monto del descuento (opcional)
    :param descripcion: Nueva descripción del descuento (opcional)
    :return: Objeto Descuento actualizado o None si no se encuentra
    """
    descuento = Descuento.objects.filter(id_descuento=id_descuento).first()
    if descuento:
        if nombre is not None:
            descuento.nombre = nombre
        if monto is not None:
            descuento.monto = monto
        if descripcion is not None:
            descuento.descripcion = descripcion
        descuento.save()
    return descuento

def eliminarDescuento(id_descuento):
    """
    Elimina un descuento de la base de datos.
    :param id_descuento: ID del descuento a eliminar
    :return: True si se eliminó correctamente, False si no se encontró
    """
    descuento = Descuento.objects.filter(id_descuento=id_descuento).first()
    if descuento:
        descuento.delete()
        return True
    return False