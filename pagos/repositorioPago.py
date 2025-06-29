from main.models import Pago

def crearPago(tipo, fecha, cliente, total_a_pagar):
    """
    Crea un nuevo pago en la base de datos.
    """
    pago = Pago(
        tipo=tipo,
        fecha=fecha,
        cliente=cliente,
        total_a_pagar=total_a_pagar
    )
    pago.save()
    return pago

def crearPagoSinCliente(tipo, fecha, total_a_pagar):
    """
    Crea un nuevo pago sin cliente específico (venta directa).
    """
    pago = Pago(
        tipo=tipo,
        fecha=fecha,
        cliente=None,  # Sin cliente específico
        total_a_pagar=total_a_pagar
    )
    pago.save()
    return pago

def obtenerUltimoPagoPorCliente(cliente):
    """
    Obtiene el último pago registrado para un cliente.
    """
    try:
        return Pago.objects.filter(cliente=cliente).latest('fecha')
    except Pago.DoesNotExist:
        return None

def obtenerPagos():
    """
    Obtiene todos los pagos de la base de datos.
    """
    return Pago.objects.all()

def obtenerPagoPorId(id_pago):
    """
    Obtiene un pago específico por su ID.
    """
    try:
        return Pago.objects.get(id_pago=id_pago)
    except Pago.DoesNotExist:
        return None

def obtenerPagosPorCliente(cliente):
    """
    Obtiene todos los pagos asociados a un cliente específico.
    """
    return Pago.objects.filter(cliente=cliente)

def actualizarPago(id_pago, tipo=None, fecha=None, cliente=None, total_a_pagar=None):
    """
    Actualiza los datos de un pago existente.
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
    """
    pago = obtenerPagoPorId(id_pago)
    if not pago:
        return False

    pago.delete()
    return True
