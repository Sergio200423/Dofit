from datetime import date
from main.repositorio.repositorioProductos import crearProducto

def validarCamposProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, estado):
    """
    Valida los campos antes de crear un producto.
    :param nombre_producto: Nombre del producto
    :param precio: Precio del producto
    :param descripcion: Descripción del producto
    :param fecha_ingreso: Fecha de ingreso del producto
    :param existencia: Cantidad en existencia del producto
    :param tipo: Tipo del producto
    :param estado: Estado del producto
    :return: (bool, str) -> True si los datos son válidos, False y un mensaje de error en caso contrario
    """
    # Validar que no haya campos vacíos
    if not nombre_producto or not descripcion or not tipo or not estado or not precio or not existencia or not fecha_ingreso:
        return False, "Todos los campos deben estar completos."

    return True, "Datos válidos."

def validarPrecio(precio):
    """
    Valida que el precio no sea cero ni menor a cero.
    """
    if precio is None or precio <= 0:
        return False, "El precio debe ser mayor a cero."
    return True, ""

def validarCantidad(cantidad):
    """
    Valida que la cantidad no sea negativa.
    """
    if cantidad is None or cantidad < 0:
        return False, "La cantidad en existencia no puede ser negativa."
    return True, ""

def validarFechaIngreso(fecha_ingreso):
    """
    Valida que la fecha de ingreso no sea menor a la fecha actual ni una fecha futura.
    """
    if fecha_ingreso is None:
        return False, "La fecha de ingreso es obligatoria."
    if fecha_ingreso < date.today():
        return False, "La fecha de ingreso no puede ser menor a la fecha actual."
    if fecha_ingreso > date.today():
        return False, "La fecha de ingreso no puede ser una fecha futura."
    return True, ""

def registrarProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, estado):
    """
    Registra un producto después de validar los datos.
    :param nombre_producto: Nombre del producto
    :param precio: Precio del producto
    :param descripcion: Descripción del producto
    :param fecha_ingreso: Fecha de ingreso del producto
    :param existencia: Cantidad en existencia del producto
    :param tipo: Tipo del producto
    :param estado: Estado del producto
    :return: (bool, str) -> True si el producto se creó correctamente, False y un mensaje de error en caso contrario
    """
    # Validar los campos básicos
    valido, mensaje = validarCamposProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, estado)
    if not valido:
        return False, mensaje

    # Validar el precio
    valido, mensaje = validarPrecio(precio)
    if not valido:
        return False, mensaje

    # Validar la cantidad
    valido, mensaje = validarCantidad(existencia)
    if not valido:
        return False, mensaje

    # Validar la fecha de ingreso
    valido, mensaje = validarFechaIngreso(fecha_ingreso)
    if not valido:
        return False, mensaje

    # Crear el producto en la base de datos
    try:
        producto = crearProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, estado)
        return True, f"Producto '{producto.nombre_producto}' registrado exitosamente."
    except Exception as e:
        return False, f"Error al registrar el producto: {str(e)}"

def validarExistencia():
    """
    Placeholder para validar la existencia de un producto.
    Esta función será implementada después de configurar repositorioPago y servicioPago.
    """
    pass