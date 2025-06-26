from datetime import datetime, date
from productos import repositorioProductos as rp

def validarCamposProducto(nombre_producto, precio, descripcion, fecha_ingreso, tipo, existencia):
    """
    Valida que los campos obligatorios estén completos.
    """
    if not nombre_producto or not descripcion or not tipo or not precio  or not fecha_ingreso or not existencia:
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
    """
    Valida que la fecha de ingreso no sea una fecha futura.
    """
    try:
        # Convierte la fecha_ingreso de str a datetime.date
        fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d').date()
    except ValueError:
        return False, "La fecha de ingreso no tiene un formato válido (YYYY-MM-DD)."

    if fecha_ingreso < date.today():
        return False, "La fecha de ingreso no puede ser anterior a la fecha actual."

    return True, "Fecha de ingreso válida."

def registrarProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, imagen=None):
    # Normalizar tipo: convertir etiqueta legible a valor de base de datos si es necesario
    # Buscar el valor correspondiente si el usuario envía la etiqueta (con acento)
    tipos_productos = rp.obtenerTiposDeProductos()
    tipo_valor = None
    for value in tipos_productos:
        if tipo == value:
            tipo_valor = value
            break
    if not tipo_valor:
        tipo_valor = tipo  # fallback, pero debería ser uno válido
    valido, mensaje = validarCamposProducto(nombre_producto, precio, descripcion, fecha_ingreso, tipo_valor, existencia)
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
        producto = rp.crearProducto(
            nombre_producto=nombre_producto,
            precio=precio,
            descripcion=descripcion,
            fecha_ingreso=fecha_ingreso,
            tipo=tipo_valor,
            existencia=existencia,
            imagen=imagen
        )
        return True, f"Producto '{producto.nombre_producto}' registrado exitosamente."
    except Exception as e:
        return False, f"Error al registrar el producto: {str(e)}"
    
def validarExistencia(producto_id, cantidad):
    """
    Valida que el producto exista y que haya suficiente stock para la cantidad solicitada.
    :param producto_id: ID del producto
    :param cantidad: Cantidad solicitada
    :return: (bool, str) -> True si hay suficiente stock, False y mensaje de error si no
    """
    producto = rp.obtenerProductoPorId(producto_id)
    if not producto:
        return False, f"El producto con ID {producto_id} no existe."
    if cantidad is None or cantidad <= 0:
        return False, "La cantidad debe ser mayor a cero."
    if producto.existencia is None or producto.existencia < cantidad:
        return False, f"Stock insuficiente para '{producto.nombre_producto}'. Disponible: {producto.existencia}, solicitado: {cantidad}."
    return True, "Stock suficiente."

def prepararVistaProductosBarraEnergetica():
    """
    Prepara los datos de productos del tipo 'Barra energética' para la vista.
    """
    productos = rp.obtenerProductosBarraEnergetica()
    productos_vista = []
    estados = rp.obtenerEstadosDeProductos()
    for producto in productos:
        productos_vista.append({
            'id_producto': producto.id_producto,
            'nombre_producto': producto.nombre_producto,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'fecha_ingreso': producto.fecha_ingreso.strftime('%Y-%m-%d'),
            'existencia': producto.existencia,
            'tipo': producto.tipo,
            'estado': producto.estado,
            'ESTADOS': estados,
        })
    return productos_vista


def prepararVistaProductosProteina():
    """
    Prepara los datos de productos del tipo 'Proteína' para la vista.
    """
    productos = rp.obtenerProductosProteina()
    productos_vista = []
    estados = rp.obtenerEstadosDeProductos()
    for producto in productos:
        productos_vista.append({
            'id_producto': producto.id,
            'nombre_producto': producto.nombre_producto,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'fecha_ingreso': producto.fecha_ingreso.strftime('%Y-%m-%d'),
            'existencia': producto.existencia,
            'tipo': producto.tipo,
            'estado': producto.estado,
            'ESTADOS': estados,
        })
    return productos_vista


def prepararVistaProductosVitaminas():
    """
    Prepara los datos de productos del tipo 'Vitaminas' para la vista.
    """
    productos = rp.btenerProductosVitaminas()
    productos_vista = []
    estados = rp.obtenerEstadosDeProductos()
    for producto in productos:
        productos_vista.append({
            'id_producto': producto.id,
            'nombre_producto': producto.nombre_producto,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'fecha_ingreso': producto.fecha_ingreso.strftime('%Y-%m-%d'),
            'existencia': producto.existencia,
            'tipo': producto.tipo,
            'estado': producto.estado,
            'ESTADOS': estados,
        })
    return productos_vista


def prepararVistaProductosSuplementos():
    """
    Prepara los datos de productos del tipo 'Suplementos' para la vista.
    """
    productos = rp.obtenerProductosSuplementos()
    productos_vista = []
    estados = rp.obtenerEstadosDeProductos()
    for producto in productos:
        productos_vista.append({
            'id_producto': producto.id,
            'nombre_producto': producto.nombre_producto,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'fecha_ingreso': producto.fecha_ingreso.strftime('%Y-%m-%d'),
            'existencia': producto.existencia,
            'tipo': producto.tipo,
            'estado': producto.estado,
            'ESTADOS': estados,
        })
    return productos_vista


def prepararVistaProductosBebidas():
    """
    Prepara los datos de productos del tipo 'Bebidas' para la vista.
    """
    productos = rp.obtenerProductosBebidas()
    productos_vista = []
    estados = rp.obtenerEstadosDeProductos()
    for producto in productos:
        productos_vista.append({
            'id_producto': producto.id,
            'nombre_producto': producto.nombre_producto,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'fecha_ingreso': producto.fecha_ingreso.strftime('%Y-%m-%d'),
            'existencia': producto.existencia,
            'tipo': producto.tipo,
            'estado': producto.estado,
            'ESTADOS': estados,
        })
    return productos_vista


def prepararVistaProductosCaramelos():
    """
    Prepara los datos de productos del tipo 'Caramelos' para la vista.
    """
    productos = rp.obtenerProductosCaramelos()
    productos_vista = []
    estados = rp.obtenerEstadosDeProductos()
    for producto in productos:
        productos_vista.append({
            'id_producto': producto.id,
            'nombre_producto': producto.nombre_producto,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'fecha_ingreso': producto.fecha_ingreso.strftime('%Y-%m-%d'),
            'existencia': producto.existencia,
            'tipo': producto.tipo,
            'estado': producto.estado,
            'ESTADOS': estados,
        })
    return productos_vista


def prepararVistaProductos():
    """
    Prepara los datos de todos los productos para la vista, sin repetir productos aunque haya varias ventas del mismo.
    """
    productos = rp.obtenerProductos()  # Obtiene todos los productos del repositorio
    productos_vista = []
    ids_agregados = set()
    estados = rp.obtenerEstadosDeProductos()
    for producto in productos:
        if producto.id_producto in ids_agregados:
            continue  # No repetir productos
        # Estado visual según existencia
        if producto.existencia == 0:
            estado = 'agotado'
        else:
            estado = 'disponible'
        productos_vista.append({
            'id_producto': producto.id_producto,
            'nombre_producto': producto.nombre_producto,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'fecha_ingreso': producto.fecha_ingreso.strftime('%Y-%m-%d') if producto.fecha_ingreso else '',
            'existencia': producto.existencia,
            'tipo': producto.tipo,
            'estado': estado,
            'imagen': producto.imagen.url if producto.imagen else None,
            'ESTADOS': estados,
        })
        ids_agregados.add(producto.id_producto)
    # DEPURACIÓN: Mostrar el primer producto serializado
    if productos_vista:
        print('DEBUG prepararVistaProductos primer producto:', productos_vista[0])
    else:
        print('DEBUG prepararVistaProductos: No hay productos')
    return productos_vista