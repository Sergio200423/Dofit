from django.core.mail import send_mail

def enviar_correo_recuperacion(correo, codigo):
    """
    Envía un correo de recuperación de contraseña con el código de verificación.
    Retorna True si el correo fue enviado correctamente, False en caso contrario.
    """
    try:
        resultado = send_mail(
            'Recuperar contraseña',
            f'Tu codigo de verificacion es: {codigo}',
            'sergiodanielxd2004@gmail.com',
            [correo],
            fail_silently=False,
        )
        return resultado > 0
    except Exception as e:
        return False, str(e)
