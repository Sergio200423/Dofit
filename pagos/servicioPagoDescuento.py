from pagos import repositorioPagoDescuento as rpd
from main.models import Pago, Descuento
from clientes import servicioClientes as sc
from clientes import repositorioMembresiaCliente as rmc

def validarPagoExistente(pago):
    """
    Valida que el pago exista en la base de datos.
    :param pago: Objeto Pago
    :return: (bool, str) -> True si el pago es válido, False y un mensaje de error en caso contrario
    """
    if not isinstance(pago, Pago):
        return False, "El objeto proporcionado no es un pago válido."
    if not Pago.objects.filter(id_pago=pago.id_pago).exists():
        return False, "El pago no existe en la base de datos."
    return True, ""

def validarDescuentoExistente(descuento):
    """
    Valida que el descuento exista en la base de datos.
    :param descuento: Objeto Descuento
    :return: (bool, str) -> True si el descuento es válido, False y un mensaje de error en caso contrario
    """
    if not isinstance(descuento, Descuento):
        return False, "El objeto proporcionado no es un descuento válido."
    if not Descuento.objects.filter(id_descuento=descuento.id_descuento).exists():
        return False, "El descuento no existe en la base de datos."
    return True, ""

def validarRelacionDuplicada(pago, descuento):
    """
    Valida que no exista una relación duplicada entre el pago y el descuento.
    :param pago: Objeto Pago
    :param descuento: Objeto Descuento
    :return: (bool, str) -> True si no hay duplicados, False y un mensaje de error en caso contrario
    """
    if rpd.obtenerDescuentosPorPago(pago).filter(descuento=descuento).exists():
        return False, "Ya existe una relación entre este pago y este descuento."
    return True, ""


def registrarPagoDescuentos(pago, descuento):
    """
    Registra una relación entre un pago y un descuento después de validar los datos
    y aplica el descuento al total del pago si corresponde.
    :param pago: Objeto Pago
    :param descuento: Objeto Descuento
    :return: (bool, str) -> True si la relación se creó correctamente, False y un mensaje de error en caso contrario
    """
    print("Iniciando la función registrarPagoDescuentos...")
    print(f"Pago recibido: {pago}")
    print(f"Descuento recibido: {descuento}")

    # Validar que el pago exista
    valido, mensaje = validarPagoExistente(pago)
    if not valido:
        print(f"Error en validarPagoExistente: {mensaje}")
        return False, mensaje

    print("Validación de pago exitosa.")

    # Validar que el descuento exista
    valido, mensaje = validarDescuentoExistente(descuento)
    if not valido:
        print(f"Error en validarDescuentoExistente: {mensaje}")
        return False, mensaje

    print("Validación de descuento exitosa.")

    # Validar que no exista una relación duplicada
    valido, mensaje = validarRelacionDuplicada(pago, descuento)
    if not valido:
        print(f"Error en validarRelacionDuplicada: {mensaje}")
        return False, mensaje

    print("Validación de relación duplicada exitosa.")

    # Validar si el cliente es estudiante (si aplica)
    if descuento.nombre.lower() == "estudiante":
        print("El descuento es para estudiantes. Validando si el cliente es estudiante...")
        valido, mensaje = sc.validarEstudiante(pago.cliente.estudiante)
        if not valido:
            print(f"Advertencia: {mensaje}")
            return None, "El cliente no es estudiante. No se aplicará el descuento."

        print("Validación de estudiante exitosa.")

    # Validar que la membresía sea mensual
    membresia_activa = rmc.obtener_membresia_activa(pago.cliente.id_cliente)
    if not membresia_activa["success"]:
        print(f"Advertencia: {membresia_activa['error']}")
        return None, "El cliente no tiene una membresía activa. No se aplicará el descuento."

    if membresia_activa["membresia_activa"].membresia.nombreMembresia.lower() != "mensual":
        print("Advertencia: El cliente no tiene una membresía mensual activa. No se aplicará el descuento.")
        return None, "El cliente no tiene una membresía mensual activa. No se aplicará el descuento."

    print("El cliente tiene una membresía mensual activa. Procediendo con el descuento.")

    # Crear la relación en la base de datos
    try:
        print("Creando la relación Pago-Descuento en la base de datos...")
        pago_descuento = rpd.crearPagoDescuento(pago, descuento)
        print(f"Relación Pago-Descuento creada exitosamente: {pago_descuento}")

        # Aplicar el descuento al total del pago
        print("Aplicando el descuento al total del pago...")
        pago_descuento.aplicar_descuento()
        print(f"Descuento aplicado correctamente. Total actualizado del pago: {pago.total_a_pagar}")

        return True, f"Relación Pago-Descuento creada exitosamente y descuento aplicado: {pago_descuento}"
    except Exception as e:
        print(f"Error al registrar la relación Pago-Descuento: {str(e)}")
        return False, f"Error al registrar la relación Pago-Descuento: {str(e)}"