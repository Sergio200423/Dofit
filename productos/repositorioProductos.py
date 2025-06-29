from main.models import Producto

def crearProducto(nombre_producto, precio, descripcion, fecha_ingreso, tipo, existencia, imagen=None):
    """
    Crea un nuevo producto en la base de datos.
    """
    producto = Producto.objects.create(
        nombre_producto=nombre_producto,
        precio=precio,
        descripcion=descripcion,
        fecha_ingreso=fecha_ingreso,
        existencia=existencia,
        tipo=tipo,
        estado='disponible',
        imagen=imagen,
    )
    return producto

def actualizarProducto(producto_id, nombre_producto, precio, existencia, descripcion, tipo, imagen=None):
    """
    Actualiza un producto existente en la base de datos.
    """
    try:
        producto = Producto.objects.get(id_producto=producto_id)
        
        # Actualizar campos
        if nombre_producto is not None:
            producto.nombre_producto = nombre_producto
        if precio is not None:
            producto.precio = precio
        if existencia is not None:
            producto.existencia = existencia
        if descripcion is not None:
            producto.descripcion = descripcion
        if tipo is not None:
            producto.tipo = tipo
        if imagen is not None:
            producto.imagen = imagen
            
        # Actualizar estado basado en existencia
        if existencia == 0:
            producto.estado = 'agotado'
        elif existencia < 10:
            producto.estado = 'pocas_unidades'
        else:
            producto.estado = 'disponible'
            
        producto.save()
        return True, f"Producto '{producto.nombre_producto}' actualizado exitosamente."
        
    except Producto.DoesNotExist:
        return False, "El producto no existe."
    except Exception as e:
        return False, f"Error al actualizar el producto: {str(e)}"

def obtenerProductos():
    """
    Obtiene todos los productos de la base de datos.
    """
    return Producto.objects.all()

def obtenerTiposDeProductos():
    """
    Obtiene los tipos de productos definidos en el modelo Producto.
    """
    return [tipo[0] for tipo in Producto.TIPOS]

def obtenerProductosPorTipo(tipo_producto):
    """
    Obtiene todos los productos de un tipo específico.
    """
    return Producto.objects.filter(tipo=tipo_producto)

def obtenerProductosBarraEnergetica():
    """
    Obtiene todos los productos del tipo 'Barra energética'.
    """
    return obtenerProductosPorTipo('Barra energetica')

def obtenerProductosProteina():
    """
    Obtiene todos los productos del tipo 'Proteína'.
    """
    return obtenerProductosPorTipo('Proteina')

def obtenerProductosVitaminas():
    """
    Obtiene todos los productos del tipo 'Vitaminas'.
    """
    return obtenerProductosPorTipo('Vitaminas')

def obtenerProductosSuplementos():
    """
    Obtiene todos los productos del tipo 'Suplementos'.
    """
    return obtenerProductosPorTipo('Suplementos')

def obtenerProductosBebidas():
    """
    Obtiene todos los productos del tipo 'Bebidas'.
    """
    return obtenerProductosPorTipo('Bebidas')

def obtenerProductosCaramelos():
    """
    Obtiene todos los productos del tipo 'Caramelos'.
    """
    return obtenerProductosPorTipo('Caramelos')

def obtenerProductoPorId(id_producto):
    """
    Obtiene un producto específico por su ID.
    """
    try:
        return Producto.objects.get(id_producto=id_producto)
    except Producto.DoesNotExist:
        return None

def obtenerEstadosDeProductos():
    """
    Obtiene los estados de productos definidos en el modelo Producto.
    """
    return Producto.ESTADOS
