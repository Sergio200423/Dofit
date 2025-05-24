from main.repositorio.repositorioPagoProductos import crearPagoProducto
from main.servicio.servicioProducto import validarExistencia

def registrarPagoProducto(pago, producto, fecha_pago, cantidad):
    """
    Registra un PagoProducto después de validar los datos.
    :param pago: Objeto Pago asociado
    :param producto: Objeto Producto asociado
    :param fecha_pago: Fecha del pago
    :param cantidad: Cantidad de productos
    :return: (bool, str) -> True si el PagoProducto se creó correctamente, False y un mensaje de error en caso contrario
    """
    # Validar la existencia del producto
    valido, mensaje = validarExistencia(producto.id_producto, cantidad)
    if not valido:
        return False, mensaje

    # Crear el PagoProducto
    try:
        pago_producto = crearPagoProducto(
            pago=pago,
            producto=producto,
            fecha_pago=fecha_pago,
            cantidad=cantidad
        )
        return True, f"PagoProducto registrado exitosamente: {pago_producto}."
    except Exception as e:
        return False, f"Error al registrar el PagoProducto: {str(e)}"
