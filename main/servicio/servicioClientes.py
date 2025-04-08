from datetime import datetime
from main.repositorio import repositorioCliente as rc

def validarFechaNacimiento(fecha_nacimiento):
    """
    Valida si la fecha de nacimiento es mayor a 14 años desde la fecha actual.
    :param fecha_nacimiento: Fecha de nacimiento en formato 'YYYY-MM-DD'
    :return: True si es mayor de edad, False si no lo es
    """
    try: 
        fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        edad = (datetime.now().date() - fecha_nacimiento_dt).days // 365
        if edad < 14:
            return False, 'La edad mínima es 14 años.'
        return True, ''
    except ValueError:
        return False, 'Formato de fecha inválido. Debe ser YYYY-MM-DD.'
    
def validarClientesRepetidos(nombre, fecha_nacimiento):
    """
    Valida si el cliente ya existe en la base de datos.
    """
    # Obtener la lista de clientes existentes
    clientes = rc.obtenerClientes()
    for cliente in clientes:
        if cliente.nombre == nombre and cliente.fecha_nacimiento == fecha_nacimiento:
            return False, 'El cliente ya existe.'
    return True, ''

def validarCamposVacios(nombre, fecha_nacimiento, sexo, fecha_inicio):
    """
    Valida si los campos de entrada están vacíos.
    :param nombre: Nombre del cliente
    :param fecha_nacimiento: Fecha de nacimiento del cliente
    :param sexo: Sexo del cliente
    :param fecha_inicio: Fecha de inicio de membresía
    :return: True si todos los campos están completos, False si alguno está vacío
    """
    if not nombre or not fecha_nacimiento or not sexo or not fecha_inicio:
        return False, 'Todos los campos son obligatorios.'
    return True, ''

def registrarClientes(nombre, fecha_nacimiento, sexo, fecha_inicio, membresia):
    """
    Registra un cliente después de validar los datos.
    :param nombre: Nombre del cliente
    :param fecha_nacimiento: Fecha de nacimiento del cliente
    :param sexo: Sexo del cliente
    :param fecha_inicio: Fecha de inicio de membresía
    :param membresia: Membresía del cliente
    :return: (bool, str) -> True si el cliente se creó correctamente, False y un mensaje de error en caso contrario
    """
    # Validar campos vacíos
    valido, mensaje = validarCamposVacios(nombre, fecha_nacimiento, sexo, fecha_inicio)
    if not valido:
        return False, mensaje

    # Validar fecha de nacimiento
    valido, mensaje = validarFechaNacimiento(fecha_nacimiento)
    if not valido:
        return False, mensaje

    # Validar si el cliente ya existe
    valido, mensaje = validarClientesRepetidos(nombre, fecha_nacimiento)
    if not valido:
        return False, mensaje

    # Crear el cliente en la base de datos
    try:
        cliente = rc.crearCliente(nombre, fecha_nacimiento, sexo, fecha_inicio, membresia)
        return True, f"Cliente '{cliente.nombre}' registrado exitosamente."
    except Exception as e:
        return False, f"Error al registrar el cliente: {str(e)}"