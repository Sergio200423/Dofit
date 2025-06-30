from datetime import datetime, date
from clientes import repositorioMembresiaCliente as rmc
from membresias import repositorioMembresia as rm
from pagos.repositorioPago import crearPago
from productos import servicioProducto as sp

def validarCamposPago(tipo, fecha, cliente, items):
    if not tipo:
        print("Error: El campo 'tipo' está vacío.")
        return False, "El campo 'tipo' es obligatorio."
    if not fecha:
        print("Error: El campo 'fecha' está vacío.")
        return False, "El campo 'fecha' es obligatorio."
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()  # Convierte la fecha a datetime.date
    except ValueError:
        print("Error: El formato de la fecha es inválido.")
        return False, "El formato de la fecha debe ser 'YYYY-MM-DD'."
    if fecha > date.today():
        print(f"Error: La fecha del pago '{fecha}' es una fecha futura.")
        return False, "La fecha del pago no puede ser una fecha futura."
    if not cliente:
        print("Error: El campo 'cliente' está vacío.")
        return False, "El campo 'cliente' es obligatorio."
    if not items:
        print("Error: El campo 'items' está vacío.")
        return False, "Debe proporcionar productos o membresías asociadas al pago."
    if tipo not in ['Membresia', 'Producto']:
        print(f"Error: El tipo de pago '{tipo}' no es válido.")
        return False, "El tipo de pago debe ser 'Membresia' o 'Producto'."
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
        # Validar existencia del producto (usar id_producto, no el objeto)
        valido, mensaje = sp.validarExistencia(producto.id_producto, cantidad)
        if not valido:
            raise ValueError(mensaje)
        total += producto.precio * cantidad
    return total
    
def calcularTotalMembresia(cliente):
    """
    Calcula el total a pagar para la membresía de un cliente utilizando el RepositorioMembresiaCliente.
    :param cliente: Objeto Cliente
    :return: Total a pagar por la membresía
    """
    # Obtener las membresías activas del cliente
    resultado = rmc.RepositorioMembresiaCliente.obtener_membresias_cliente(cliente.id_cliente)

    if not resultado["success"]:
        raise ValueError(resultado["error"])

    # Verificar si el cliente tiene una membresía activa
    membresias = resultado["membresias"]
    membresia_activa = next((m for m in membresias if m.fecha_fin >= date.today()), None)

    if not membresia_activa:
        raise ValueError("El cliente no tiene una membresía activa.")

    # Retornar el precio de la membresía activa
    return membresia_activa.membresia.precio

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
    print("Iniciando la función registrarPago...")
    print(f"Registrando pago: tipo={tipo}, fecha={fecha}, cliente={cliente}, productos={productos}, renovar_membresia={renovar_membresia}")

    # Validar campos básicos
    items = productos if productos else []
    if renovar_membresia:
        items.append("Membresia")
    valido, mensaje = validarCamposPago(tipo, fecha, cliente, items)
    if not valido:
        print(f"Error en la validación de campos: {mensaje}")
        return False, mensaje

    # Calcular el total a pagar
    total_a_pagar = 0
    try:
        if tipo == 'Producto' or tipo == 'Ambos':
            if not productos:
                print("Error: No se proporcionaron productos para el pago de tipo 'Producto'.")
                return False, "Debe proporcionar productos para el pago de tipo 'Producto'."
            total_productos = calcularTotalProductos(productos)
            print(f"Total calculado para productos: {total_productos}")
            total_a_pagar += total_productos

        if tipo == 'Membresia' or tipo == 'Ambos':
            if renovar_membresia:
                total_membresia = calcularTotalMembresia(cliente)
                print(f"Total calculado para membresía: {total_membresia}")
                total_a_pagar += total_membresia
    except ValueError as e:
        print(f"Error al calcular el total: {str(e)}")
        return False, str(e)

    # Validar que el total a pagar no sea None
    if total_a_pagar is None:
        print("Error: El total a pagar es None.")
        return False, "El total a pagar no se pudo calcular correctamente."

    print(f"Total a pagar calculado: {total_a_pagar}")

    # Crear el pago en la base de datos
    try:
        pago = crearPago(tipo=tipo, fecha=fecha, cliente=cliente, total_a_pagar=total_a_pagar)
        print(f"Pago creado exitosamente: {pago}")
        return True, f"Pago registrado exitosamente. Total a pagar: ${{total_a_pagar:.2f}}"
    except Exception as e:
        print(f"Error al registrar el pago: {str(e)}")
        return False, f"Error al registrar el pago: {str(e)}"

def registrarPagoMembresia(fecha, cliente, membresia_id, cantidad=1):
    """
    Registra un pago de membresía para un cliente.
    :param fecha: Fecha del pago (datetime.date o str)
    :param cliente: Objeto Cliente
    :param membresia_id: ID de la membresía a registrar
    :param cantidad: Cantidad de membresías (por defecto 1, normalmente siempre 1)
    :return: (bool, str) -> True si el pago y la membresía se registraron correctamente, False y mensaje de error en caso contrario
    """
    try:
        # Validar y convertir fecha si es string
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        # Validar existencia de la membresía
        membresia = rm.obtenerMembresias().filter(id_membresia=membresia_id).first()
        if not membresia:
            return False, f"No se encontró la membresía con ID {membresia_id}."
        # Calcular el total a pagar
        total_a_pagar = membresia.precio * cantidad
        # Crear el pago
        pago = crearPago(tipo="Membresia", fecha=fecha, cliente=cliente, total_a_pagar=total_a_pagar)
        # Registrar la membresía para el cliente
        resultado_membresia = rmc.crear_membresia_cliente(
            id_cliente=cliente.id_cliente,
            id_membresia=membresia_id,
            fecha_inicio=fecha
        )
        if not resultado_membresia["success"]:
            return False, resultado_membresia["error"]
        return True, f"Pago de membresía registrado exitosamente. Total a pagar: ${total_a_pagar:.2f}"
    except Exception as e:
        return False, f"Error al registrar el pago de membresía: {str(e)}"