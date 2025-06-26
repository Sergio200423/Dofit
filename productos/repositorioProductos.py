from main.models import Producto

def crearProducto(nombre_producto, precio, descripcion, fecha_ingreso, tipo, existencia, imagen=None):
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
        estado='disponible',
        imagen=imagen,  # Guardar la imagen directamente en el create
    )
    return producto

def obtenerProductos():
    """
    Obtiene todos los productos de la base de datos.
    :return: QuerySet de objetos Producto
    """
    return Producto.objects.all()

def obtenerTiposDeProductos():
    """
    Obtiene los tipos de productos definidos en el modelo Producto.
    :return: Lista de tipos de productos
    """
    return [tipo[1] for tipo in Producto.TIPOS]

def obtenerProductosPorTipo(tipo_producto):
    """
    Obtiene todos los productos de un tipo específico.
    :param tipo_producto: Tipo de producto (por ejemplo, 'Barra energética', 'Proteína', etc.)
    :return: QuerySet de objetos Producto filtrados por tipo
    """
    return Producto.objects.filter(tipo=tipo_producto)

def obtenerProductosBarraEnergetica():
    """
    Obtiene todos los productos del tipo 'Barra energética'.
    :return: QuerySet de objetos Producto
    """
    return obtenerProductosPorTipo('Barra energética')

def obtenerProductosProteina():
    """
    Obtiene todos los productos del tipo 'Proteína'.
    :return: QuerySet de objetos Producto
    """
    return obtenerProductosPorTipo('Proteína')

def obtenerProductosVitaminas():
    """
    Obtiene todos los productos del tipo 'Vitaminas'.
    :return: QuerySet de objetos Producto
    """
    return obtenerProductosPorTipo('Vitaminas')

def obtenerProductosSuplementos():
    """
    Obtiene todos los productos del tipo 'Suplementos'.
    :return: QuerySet de objetos Producto
    """
    return obtenerProductosPorTipo('Suplementos')

def obtenerProductosBebidas():
    """
    Obtiene todos los productos del tipo 'Bebidas'.
    :return: QuerySet de objetos Producto
    """
    return obtenerProductosPorTipo('Bebidas')

def obtenerProductosCaramelos():
    """
    Obtiene todos los productos del tipo 'Caramelos'.
    :return: QuerySet de objetos Producto
    """
    return obtenerProductosPorTipo('Caramelos')

def obtenerProductoPorId(id_producto):
    """
    Obtiene un producto específico por su ID.
    :param id_producto: ID del producto
    :return: Objeto Producto o None si no se encuentra
    """
    try:
        return Producto.objects.get(id_producto=id_producto)
    except Producto.DoesNotExist:
        return None

def obtenerEstadosDeProductos():
    """
    Obtiene los estados de productos definidos en el modelo Producto.
    :return: Lista de estados de productos
    """
    return Producto.ESTADOS