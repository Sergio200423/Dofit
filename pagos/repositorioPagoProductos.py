from main.models import PagoProducto

def crearPagoProducto(pago, producto, fecha_pago, cantidad):
    """
    Crea un nuevo registro en la tabla PagoProducto.
    :param pago: Objeto Pago asociado
    :param producto: Objeto Producto asociado
    :param fecha_pago: Fecha del pago
    :param cantidad: Cantidad de productos
    :return: Objeto PagoProducto creado
    """
    pago_producto = PagoProducto.objects.create(
        pago=pago,
        producto=producto,
        fecha_pago=fecha_pago,
        cantidad=cantidad
    )
    return pago_producto

def obtenerPagoProductos():
    """
    Obtiene todos los registros de la tabla PagoProducto.
    :return: QuerySet de objetos PagoProducto
    """
    return PagoProducto.objects.all()

def obtenerPagoProductoPorId(id_pago_producto):
    """
    Obtiene un registro específico de PagoProducto por su ID.
    :param id_pago_producto: ID del PagoProducto
    :return: Objeto PagoProducto o None si no se encuentra
    """
    try:
        return PagoProducto.objects.get(id_pago_producto=id_pago_producto)
    except PagoProducto.DoesNotExist:
        return None

def obtenerPagoProductosPorPago(pago):
    """
    Obtiene todos los productos asociados a un pago específico.
    :param pago: Objeto Pago
    :return: QuerySet de objetos PagoProducto
    """
    return PagoProducto.objects.filter(pago=pago)

def actualizarPagoProducto(id_pago_producto, cantidad=None, fecha_pago=None):
    """
    Actualiza los datos de un registro en la tabla PagoProducto.
    :param id_pago_producto: ID del PagoProducto a actualizar
    :param cantidad: Nueva cantidad de productos (opcional)
    :param fecha_pago: Nueva fecha del pago (opcional)
    :return: Objeto PagoProducto actualizado o None si no se encuentra
    """
    pago_producto = obtenerPagoProductoPorId(id_pago_producto)
    if not pago_producto:
        return None

    if cantidad is not None:
        pago_producto.cantidad = cantidad
    if fecha_pago is not None:
        pago_producto.fecha_pago = fecha_pago

    pago_producto.save()
    return pago_producto

def eliminarPagoProducto(id_pago_producto):
    """
    Elimina un registro de la tabla PagoProducto.
    :param id_pago_producto: ID del PagoProducto a eliminar
    :return: True si se eliminó correctamente, False si no se encontró
    """
    pago_producto = obtenerPagoProductoPorId(id_pago_producto)
    if not pago_producto:
        return False

    pago_producto.delete()
    return True