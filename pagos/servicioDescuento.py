from main.repositorio import repositorioDescuento as rd

def validarCamposVacios(nombre, monto):
    """
    Valida que los campos obligatorios no estén vacíos.
    :param nombre: Nombre del descuento
    :param monto: Monto del descuento
    :return: (bool, str) -> True si los campos son válidos, False y un mensaje de error en caso contrario
    """
    if not nombre or monto is None:
        return False, "El nombre y el monto son campos obligatorios."
    return True, ""

def validarMontoPositivo(monto):
    """
    Valida que el monto del descuento sea un número positivo.
    :param monto: Monto del descuento
    :return: (bool, str) -> True si el monto es válido, False y un mensaje de error en caso contrario
    """
    if monto <= 0:
        return False, "El monto del descuento debe ser un número positivo."
    return True, ""

def validarDescuentoRepetido(nombre):
    """
    Valida que no exista un descuento con el mismo nombre.
    :param nombre: Nombre del descuento
    :return: (bool, str) -> True si el nombre es único, False y un mensaje de error en caso contrario
    """
    descuento_existente = rd.obtenerTodosLosDescuentos().filter(nombre=nombre).first()
    if descuento_existente:
        return False, f"Ya existe un descuento con el nombre '{nombre}'."
    return True, ""

def registrarDescuentos(nombre, monto, descripcion=None):
    """
    Registra un descuento después de validar los datos.
    :param nombre: Nombre del descuento
    :param monto: Monto del descuento
    :param descripcion: Descripción opcional del descuento
    :return: (bool, str) -> True si el descuento se creó correctamente, False y un mensaje de error en caso contrario
    """
    # Validar campos vacíos
    valido, mensaje = validarCamposVacios(nombre, monto)
    if not valido:
        return False, mensaje

    # Validar que el monto sea positivo
    valido, mensaje = validarMontoPositivo(monto)
    if not valido:
        return False, mensaje

    # Validar que el nombre del descuento no esté repetido
    valido, mensaje = validarDescuentoRepetido(nombre)
    if not valido:
        return False, mensaje

    # Crear el descuento en la base de datos
    try:
        descuento = rd.crearDescuento(nombre, monto, descripcion)
        return True, f"Descuento '{descuento.nombre}' registrado exitosamente."
    except Exception as e:
        return False, f"Error al registrar el descuento: {str(e)}"