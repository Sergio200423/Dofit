from main.models import PagoDescuento

def crearPagoDescuento(pago, descuento):
    """
    Crea una nueva relación entre un pago y un descuento.
    :param pago: Objeto Pago
    :param descuento: Objeto Descuento
    :return: Objeto PagoDescuento creado
    """
    pago_descuento = PagoDescuento.objects.create(
        pago=pago,
        descuento=descuento
    )
    return pago_descuento

def obtenerTodosLosPagosDescuentos():
    """
    Obtiene todas las relaciones entre pagos y descuentos.
    :return: QuerySet de objetos PagoDescuento
    """
    return PagoDescuento.objects.all()

def obtenerPagoDescuentoPorId(id_pago_descuento):
    """
    Obtiene una relación específica entre un pago y un descuento por su ID.
    :param id_pago_descuento: ID de la relación PagoDescuento
    :return: Objeto PagoDescuento o None si no se encuentra
    """
    return PagoDescuento.objects.filter(id_pago_descuento=id_pago_descuento).first()

def obtenerDescuentosPorPago(pago):
    """
    Obtiene todos los descuentos aplicados a un pago específico.
    :param pago: Objeto Pago
    :return: QuerySet de objetos PagoDescuento relacionados con el pago
    """
    return PagoDescuento.objects.filter(pago=pago)

def actualizarPagoDescuento(id_pago_descuento, pago=None, descuento=None):
    """
    Actualiza una relación entre un pago y un descuento.
    :param id_pago_descuento: ID de la relación PagoDescuento a actualizar
    :param pago: Nuevo objeto Pago (opcional)
    :param descuento: Nuevo objeto Descuento (opcional)
    :return: Objeto PagoDescuento actualizado o None si no se encuentra
    """
    pago_descuento = PagoDescuento.objects.filter(id_pago_descuento=id_pago_descuento).first()
    if pago_descuento:
        if pago is not None:
            pago_descuento.pago = pago
        if descuento is not None:
            pago_descuento.descuento = descuento
        pago_descuento.save()
    return pago_descuento

def eliminarPagoDescuento(id_pago_descuento):
    """
    Elimina una relación entre un pago y un descuento.
    :param id_pago_descuento: ID de la relación PagoDescuento a eliminar
    :return: True si se eliminó correctamente, False si no se encontró
    """
    pago_descuento = PagoDescuento.objects.filter(id_pago_descuento=id_pago_descuento).first()
    if pago_descuento:
        pago_descuento.delete()
        return True
    return False