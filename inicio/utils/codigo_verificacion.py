import time

def guardar_codigo_verificacion(session, codigo):
    session['codigo_verificacion'] = codigo
    session['codigo_verificacion_time'] = int(time.time())


def codigo_verificacion_valido(session, codigo_usuario, tiempo_max=180, intentos_max=3):
    """
    Valida si el código ingresado es correcto, no ha expirado y no se han agotado los intentos.
    Retorna (True, None) si es válido, (False, mensaje, intentos_restantes) si no.
    """
    codigo_session = str(session.get('codigo_verificacion', ''))
    codigo_time = session.get('codigo_verificacion_time', 0)
    tiempo_actual = int(time.time())
    correo = session.get('correo_usuario')
    intentos_dict = session.get('intentos_codigo', {})
    intentos_actuales = intentos_dict.get(correo, 0)

    print(f"[DEBUG][codigo_verificacion_valido] correo: {correo}")
    print(f"[DEBUG][codigo_verificacion_valido] intentos_dict antes: {intentos_dict}")
    print(f"[DEBUG][codigo_verificacion_valido] intentos_actuales: {intentos_actuales}")

    if not codigo_session:
        print(f"[DEBUG][codigo_verificacion_valido] No hay código en sesión")
        return False, 'No hay código de verificación en la sesión.', intentos_max - intentos_actuales
    if codigo_time and (tiempo_actual - int(codigo_time) > tiempo_max):
        print(f"[DEBUG][codigo_verificacion_valido] Código expirado")
        return False, 'El código ha expirado. Solicita uno nuevo.', intentos_max - intentos_actuales
    if intentos_actuales >= intentos_max:
        print(f"[DEBUG][codigo_verificacion_valido] Intentos agotados")
        return False, 'Has agotado tus intentos. Solicita un nuevo código.', 0
    if codigo_usuario.strip() != codigo_session.strip():
        intentos_actuales += 1
        intentos_dict[correo] = intentos_actuales
        session['intentos_codigo'] = intentos_dict
        print(f"[DEBUG][codigo_verificacion_valido] Código incorrecto. intentos_actuales: {intentos_actuales}")
        print(f"[DEBUG][codigo_verificacion_valido] intentos_dict después: {intentos_dict}")
        if intentos_actuales >= intentos_max:
            print(f"[DEBUG][codigo_verificacion_valido] Intentos agotados tras fallo")
            return False, 'Has agotado tus intentos. Solicita un nuevo código.', 0
        return False, 'Código incorrecto. Intenta de nuevo.', intentos_max - intentos_actuales
    # Si es válido, limpiar los intentos para ese correo
    if correo in intentos_dict:
        intentos_dict.pop(correo)
        session['intentos_codigo'] = intentos_dict
        print(f"[DEBUG][codigo_verificacion_valido] Código correcto. Limpiando intentos para {correo}")
    print(f"[DEBUG][codigo_verificacion_valido] Código válido. intentos_dict final: {intentos_dict}")
    return True, None, intentos_max - intentos_actuales
