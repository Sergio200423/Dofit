from django.contrib.auth.models import User

def validarNombreUsuario(nombreUsuario):
    try: 
        user=User.objects.get(username=nombreUsuario)
        return True
    except User.DoesNotExist:
        return False
    
def validarContraseña(nombreUsuario, contraseña):
    try:
        user = User.objects.get(username=nombreUsuario)
        return user.check_password(contraseña)
    except User.DoesNotExist:
        return False
