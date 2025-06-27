from django.contrib.auth.hashers import check_password
from usuarios.models import Usuario

ERRORCREDENCIAL = 'Usuario o contraseña incorrecta'
ERRORBLOQUEO = 'Usuario bloqueado por demasiados intentos fallidos. Contacte al administrador.'

def usuario_valido(username):
    """"Verifica si el usuario existe en la base de datos. En caso de que exista, retorna el usuario,
    en caso contrario, retorna None."""
    try:
        user = Usuario.objects.get(nombre_usuario=username)
        return user
    except Usuario.DoesNotExist:
        return None

def contrasena_valida(user, password):
    """Verifica si la contraseña proporcionada es correcta para el usuario dado."""
    if user is None:
        print(f"[LOGIN DEBUG] Usuario es None en contrasena_valida")
        return False
    print(f"[LOGIN DEBUG] Password recibido: {password} (type: {type(password)})")
    print(f"[LOGIN DEBUG] Hash en BD: {user.contra} (type: {type(user.contra)})")
    try:
        resultado = check_password(password, user.contra)
        print(f"[LOGIN DEBUG] check_password result: {resultado}")
    except Exception as e:
        print(f"[LOGIN DEBUG] ERROR en check_password: {e}")
        resultado = False
    return resultado

def manejar_intentos(user):
    """"Maneja los intentos de inicio de sesion del usuario. Si tiene menos de tres intentos,
    se le suman los intentos actuales. En caso contrario solo se devuelve el numero de intentos
    sin modificarlo."""
    if user.n_intentos < 3:
        user.n_intentos += 1
        user.save()
    return user.n_intentos

def login(username, password, n_intentos=0):
    """"Intenta iniciar sesion con el nombre de usuario y la contra proporcionada."""
    user = usuario_valido(username)
    if not user:
        # Si el usuario no existe, incrementa n_intentos localmente
        if n_intentos < 3:
            n_intentos += 1
            error_msg = ERRORCREDENCIAL

        else:
            error_msg = ERRORBLOQUEO
        return {'success': False, 'error': error_msg, 'user': None, 'n_intentos': n_intentos}

    n_intentos = user.n_intentos
    if n_intentos >= 3:
        print(f"[LOGIN DEBUG] ERROR (usuario bloqueado): {ERRORBLOQUEO} | n_intentos={n_intentos}")
        return {'success': False, 'error': ERRORBLOQUEO, 'user': user, 'n_intentos': n_intentos}
    # if getattr(user.rol, 'id', None) not in [1, 2]:
    #     n_intentos = manejar_intentos(user)
    #     return {'success': False, 'error': ERRORCREDENCIAL, 'user': user, 'n_intentos': n_intentos}
    # Comentado para pruebas de login sin validación de rol
    if contrasena_valida(user, password):
        user.n_intentos = 0
        user.save()
        print(f"[LOGIN DEBUG] EXITO: Login correcto para usuario {username} | n_intentos=0")
        return {'success': True, 'user': user, 'n_intentos': 0}
    else:
        n_intentos = manejar_intentos(user)
        error_msg = ERRORCREDENCIAL if n_intentos < 3 else ERRORBLOQUEO
        print(f"[LOGIN DEBUG] ERROR (contraseña incorrecta): {error_msg} | n_intentos={n_intentos}")
        return {'success': False, 'error': error_msg, 'user': user, 'n_intentos': n_intentos}

