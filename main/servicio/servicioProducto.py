from datetime import date
from main.repositorio.repositorioProductos import crearProducto

def validarCamposProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, estado):
    if not nombre_producto or not descripcion or not tipo or not estado or not precio or not existencia or not fecha_ingreso:
        return False, "Todos los campos deben estar completos."
    return True, "Datos válidos."

def validarPrecio(precio):
    if precio is None or precio <= 0:
        return False, "El precio debe ser mayor a cero."
    return True, ""

def validarCantidad(cantidad):
    if cantidad is None or cantidad < 0:
        return False, "La cantidad en existencia no puede ser negativa."
    return True, ""

def validarFechaIngreso(fecha_ingreso):
    if fecha_ingreso is None:
        return False, "La fecha de ingreso es obligatoria."
    if fecha_ingreso < date.today():
        return False, "La fecha de ingreso no puede ser menor a la fecha actual."
    if fecha_ingreso > date.today():
        return False, "La fecha de ingreso no puede ser una fecha futura."
    return True, ""

def registrarProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, estado):
    valido, mensaje = validarCamposProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, estado)
    if not valido:
        return False, mensaje

    valido, mensaje = validarPrecio(precio)
    if not valido:
        return False, mensaje

    valido, mensaje = validarCantidad(existencia)
    if not valido:
        return False, mensaje

    valido, mensaje = validarFechaIngreso(fecha_ingreso)
    if not valido:
        return False, mensaje

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