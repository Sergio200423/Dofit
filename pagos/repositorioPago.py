from main.models import Pago

def crearPago(tipo, fecha, cliente, total_a_pagar):
    """
    Crea un nuevo pago en la base de datos.
    :param tipo: Tipo de pago ('Membresia', 'Producto')
    :param fecha: Fecha del pago
    :param cliente: Objeto Cliente asociado al pago
    :param total_a_pagar: Total calculado manualmente (opcional)
    :return: Objeto Pago creado
    """
    # Crear el objeto Pago
    pago = Pago(
        tipo=tipo,
        fecha=fecha,
        cliente=cliente,
        total_a_pagar=total_a_pagar
    )

    pago.save()

    return pago

def obtenerUltimoPagoPorCliente(cliente):
    """
    Obtiene el último pago registrado para un cliente.
    :param cliente: Objeto Cliente
    :return: Objeto Pago si existe, None en caso contrario
    """
    try:
        return Pago.objects.filter(cliente=cliente).latest('fecha')
    except Pago.DoesNotExist:
        return None

def obtenerPagos():
    """
    Obtiene todos los pagos de la base de datos.
    :return: QuerySet de objetos Pago
    """
    return Pago.objects.all()

def obtenerPagoPorId(id_pago):
    """
    Obtiene un pago específico por su ID.
    :param id_pago: ID del pago
    :return: Objeto Pago o None si no se encuentra
    """
    try:
        return Pago.objects.get(id_pago=id_pago)
    except Pago.DoesNotExist:
        return None

def obtenerPagosPorCliente(cliente):
    """
    Obtiene todos los pagos asociados a un cliente específico.
    :param cliente: Objeto Cliente
    :return: QuerySet de objetos Pago
    """
    return Pago.objects.filter(cliente=cliente)

def actualizarPago(id_pago, tipo=None, fecha=None, cliente=None, total_a_pagar=None):
    """
    Actualiza los datos de un pago existente.
    :param id_pago: ID del pago a actualizar
    :param tipo: Nuevo tipo de pago (opcional)
    :param fecha: Nueva fecha del pago (opcional)
    :param cliente: Nuevo cliente asociado (opcional)
    :param total_a_pagar: Nuevo total a pagar (opcional)
    :return: Objeto Pago actualizado o None si no se encuentra
    """
    pago = obtenerPagoPorId(id_pago)
    if not pago:
        return None

    if tipo:
        pago.tipo = tipo
    if fecha:
        pago.fecha = fecha
    if cliente:
        pago.cliente = cliente
    if total_a_pagar is not None:
        pago.total_a_pagar = total_a_pagar

    pago.save()
    return pago

def eliminarPago(id_pago):
    """
    Elimina un pago de la base de datos.
    :param id_pago: ID del pago a eliminar
    :return: True si se eliminó correctamente, False si no se encontró
    """
    pago = obtenerPagoPorId(id_pago)
    if not pago:
        return False

    pago.delete()
    return True