from datetime import date
from main.repositorio.repositorioPago import crearPago
from main.servicio.servicioProducto import validarExistencia
from main.repositorio.repositorioMembresia import obtenerMembresiaPorCliente

def validarCamposPago(tipo, fecha, cliente, items):
    """
    Valida que los campos del pago no estén vacíos.
    :param tipo: Tipo de pago ('Membresia' o 'Producto')
    :param fecha: Fecha del pago
    :param cliente: Objeto Cliente asociado al pago
    :param items: Lista de productos o membresías asociadas al pago
    :return: (bool, str) -> True si los datos son válidos, False y un mensaje de error en caso contrario
    """
    if not tipo or not fecha or not cliente or not items:
        return False, "Todos los campos son obligatorios."
    if tipo not in ['Membresia', 'Producto']:
        return False, "El tipo de pago debe ser 'Membresia' o 'Producto'."
    if fecha > date.today():
        return False, "La fecha del pago no puede ser una fecha futura."
    return True, ""

def calcularTotalProductos(productos):
    """
    Calcula el total a pagar para productos.
    :param productos: Lista de diccionarios con 'producto' y 'cantidad'
    :return: Total a pagar por los productos
    """
    total = 0
    for item in productos:
        producto = item.get('producto')
        cantidad = item.get('cantidad', 0)
        # Validar existencia del producto
        valido, mensaje = validarExistencia(producto, cantidad)
        if not valido:
            raise ValueError(mensaje)
        total += producto.precio * cantidad
    return total

def calcularTotalMembresia(cliente):
    """
    Calcula el total a pagar para la membresía de un cliente.
    :param cliente: Objeto Cliente
    :return: Total a pagar por la membresía
    """
    membresia = obtenerMembresiaPorCliente(cliente)
    if not membresia:
        raise ValueError("El cliente no tiene una membresía activa.")
    return membresia.precio

def registrarPago(tipo, fecha, cliente, productos=None, renovar_membresia=False):
    """
    Registra un pago después de validar los datos y calcular el total.
    :param tipo: Tipo de pago ('Membresia', 'Producto' o ambos)
    :param fecha: Fecha del pago
    :param cliente: Objeto Cliente asociado al pago
    :param productos: Lista de productos con cantidades (opcional)
    :param renovar_membresia: Indica si se debe renovar la membresía (opcional)
    :return: (bool, str) -> True si el pago se creó correctamente, False y un mensaje de error en caso contrario
    """
    # Validar campos básicos
    items = productos if productos else []
    if renovar_membresia:
        items.append("Membresia")
    valido, mensaje = validarCamposPago(tipo, fecha, cliente, items)
    if not valido:
        return False, mensaje

    # Calcular el total a pagar
    total_a_pagar = 0
    try:
        if tipo == 'Producto' or tipo == 'Ambos':
            if not productos:
                return False, "Debe proporcionar productos para el pago de tipo 'Producto'."
            total_a_pagar += calcularTotalProductos(productos)
        if tipo == 'Membresia' or tipo == 'Ambos':
            if renovar_membresia:
                total_a_pagar += calcularTotalMembresia(cliente)
    except ValueError as e:
        return False, str(e)

    # Crear el pago en la base de datos
    try:
        pago = crearPago(tipo=tipo, fecha=fecha, cliente=cliente, total_a_pagar=total_a_pagar)
        return True, f"Pago registrado exitosamente. Total a pagar: ${total_a_pagar:.2f}"
    except Exception as e:
        return False, f"Error al registrar el pago: {str(e)}"