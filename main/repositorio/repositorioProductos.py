from main.models import Producto

def crearProducto(nombre_producto, precio, descripcion, fecha_ingreso, existencia, tipo, estado):
    """
    Crea un nuevo producto en la base de datos.
    :param nombre_producto: Nombre del producto
    :param precio: Precio del producto
    :param descripcion: Descripción del producto
    :param fecha_ingreso: Fecha de ingreso del producto
    :param existencia: Cantidad en existencia del producto
    :param tipo: Tipo del producto (debe coincidir con las opciones en TIPOS)
    :param estado: Estado del producto (debe coincidir con las opciones en ESTADOS)
    :return: Objeto Producto creado
    """
    producto = Producto.objects.create(
        nombre_producto=nombre_producto,
        precio=precio,
        descripcion=descripcion,
        fecha_ingreso=fecha_ingreso,
        existencia=existencia,
        tipo=tipo,
        estado=estado
    )
    return producto

def obtenerProductos():
    """
    Obtiene todos los productos de la base de datos.
    :return: QuerySet de objetos Producto
    """
    return Producto.objects.all()