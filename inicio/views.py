from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from django.contrib.messages import get_messages
from inicio.utils.validarLogin import login, usuario_valido
from django.core.mail import send_mail
from usuarios.models import Usuario
from inicio import GenerarCodigoAleatorio as gca
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    """
    Cargamos la vista de inicio de la aplicacion.
    """
    return render(request, 'inicio/inicio.html')

def inicio_sesion(request):
    """
    Cargamos la vista de inicio de sesion de la aplicacion.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        n_intentos = int(request.POST.get('n_intentos', 0))
        usuario_valido1 = usuario_valido(username)
        print(f"[LOGIN DEBUG] Usuario válido: {usuario_valido1 is not None}")
        print(f"[LOGIN DEBUG] Intentando iniciar sesión: usuario={username}, n_intentos={n_intentos}, contra={password}")

        result = login(username, password, n_intentos)
        user = result.get('user')
        n_intentos = result.get('n_intentos', 0)

        if result['success']:

            # Login exitoso
            request.session['usuario_id'] = user.id_usuario
            request.session['usuario_nombre'] = user.nombre_usuario
            request.session['usuario_rol'] = user.rol.nombre
            return redirect('clientes:principal')
        else:

            error_msg = result.get('error', 'Error desconocido')
            messages.error(request, error_msg)

            return render(request, 'inicio/login.html', {'n_intentos': n_intentos})
    return render(request, 'inicio/login.html', {'n_intentos': 0})

def nueva_contrasena(request):
    """
    Cargamos la vista de nueva contrasena de la aplicacion.
    """
    return render(request, 'inicio/nueva_contraseña.html')

def recuperar_contrasena(request):
    if request.method == 'POST':
        print('[DEBUG] Se recibió un POST en recuperar_contraseña_view')
        # Obtener el correo del usuario seleccionado desde el formulario
        correo = request.POST.get('correo')
        print(f'[DEBUG] Valor recibido en correo: {correo}')
        if correo:
            # Generar código de verificación
            codigo = gca.generar_codigo_verificacion()
            print(f'[DEBUG] Código generado: {codigo}')
            # Guardar en sesión
            request.session['correo_usuario'] = correo
            request.session['codigo_verificacion'] = codigo
            # Enviar correo
            try:
                resultado = send_mail(
                    'Recuperar contraseña',
                    f'Tu codigo de verificacion es: {codigo}',
                    'sergiodanielxd2004@gmail.com',
                    [correo],
                    fail_silently=False,
                )
                print(f'[DEBUG] Resultado de send_mail: {resultado}')
            except Exception as e:
                print(f'[DEBUG] Excepción al enviar correo: {e}')
                messages.error(request, f'Error al enviar el correo: {e}')
                return redirect('recuperar_contra')
            if resultado > 0:
                print('[DEBUG] Redirigiendo a email_enviado')
                return redirect('email_enviado')
            else:
                messages.error(request, 'Error al enviar el correo')
                print('[DEBUG] Error: send_mail retornó 0')
                return redirect('recuperar_contra')
        else:
            messages.error(request, 'No se seleccionó ningún usuario')
            print('[DEBUG] No se seleccionó ningún usuario')
            return redirect('recuperar_contra')
    # GET: mostrar la lista de usuarios
    usuarios = Usuario.objects.all()
    return render(request, 'inicio/recuperar_contra.html', {'usuarios': usuarios})

def reenviar_correo(request):
    # Recuperamos el correo de la sesión
    correo = request.session.get('correo_usuario')
    codigo = request.session.get('codigo_verificacion')

    if correo:
        # Reenviamos el correo
        resultado = send_mail(
            'Recuperar contraseña',
            f'Tu codigo de verificacion es: {codigo}',
            'sergiodanielxd2004@gmail.com',
            [correo],
            fail_silently=False,
        )

        if resultado > 0:
            messages.success(request, 'Correo reenviado correctamente')
        else:
            messages.error(request, 'Error al reenviar el correo')
    else:
        messages.error(request, 'No se encontró un correo para reenviar')

    return redirect('email_enviado')

def recuperar_contra_password(request):
    #Validamos si el metodo es POST
    if request.method == 'POST':
        #Obtenemos el correo del usuario ingresado por el usuario
        correo = request.POST.get('correo')
        codigo = gca.generar_codigo_verificacion()

        request.session['correo_usuario'] = correo
        request.session['codigo_verificacion'] = codigo
        
        #Procesamos el correo con el modulo de python "send mail"
        resultado = send_mail(
            'Recuperar contraseña',
            f'Tu codigo de verificacion es: {codigo}',
            'sergiodanielxd2004@gmail.com',
            [correo],
            fail_silently=False,
        )

        if resultado > 0:
            return redirect('email_enviado')
        else:    
            messages.error(request, 'Error al enviar el correo')
            return redirect('recuperar_contra_password')
    return render(request, 'inicio/recuperar_contra_password.html')

@require_http_methods(["GET", "POST"])
def email_enviado(request):
    if request.method == "POST":
        # Aquí puedes procesar el código ingresado por el usuario
        # Por ejemplo, validar el código y redirigir según corresponda
        # codigo = request.POST.getlist('primerNumero', ...) # Combina los 4 inputs
        # Lógica de validación aquí
        pass
    return render(request, 'inicio/email_enviado.html')

def nueva_contraseña(request):
    if request.method == 'POST':
        contra = request.POST.get('contraseña')
        confirmar_contra = request.POST.get('confirmar_contraseña')

        # Nueva validación: la contraseña no debe ser igual a la actual
        correo_usuario = request.session.get('correo_usuario')
        if correo_usuario:
            try:
                usuario = Usuario.objects.get(correo=correo_usuario)
                if check_password(contra, usuario.contra):
                    messages.error(request, 'La nueva contraseña no puede ser igual a la actual.')
                    return render(request, 'inicio/nueva_contraseña.html', {"error_contra_igual": True})
            except Usuario.DoesNotExist:
                messages.error(request, 'No se encontró el usuario para actualizar la contraseña.')
                return render(request, 'inicio/nueva_contraseña.html')

        if contra != confirmar_contra:
            messages.error(request, 'Las contraseñas no coinciden')
        else:
            # Obtener el correo del usuario desde la sesión
            correo_usuario = request.session.get('correo_usuario')
            if correo_usuario:
                try:
                    usuario = Usuario.objects.get(correo=correo_usuario)
                    usuario.contra = make_password(contra)
                    usuario.n_intentos = 0  # Restablecer intentos fallidos al cambiar la contraseña
                    usuario.save()

                    # Cierra todas las sesiones activas del usuario (si aplica)
                    sessions = Session.objects.all()
                    for session in sessions:
                        data = session.get_decoded()
                        if data.get('usuario_id') == usuario.id_usuario:
                            session.delete()

                    # Limpiar mensajes antes de redirigir al login
                    storage = get_messages(request)
                    for _ in storage:
                        pass  # Consumir todos los mensajes

                    messages.success(request, 'Contraseña actualizada correctamente. Todas las sesiones han sido cerradas.')
                    return redirect('inicio_sesion')
                except Usuario.DoesNotExist:
                    messages.error(request, 'No se encontró el usuario para actualizar la contraseña.')
            else:
                messages.error(request, 'No se encontró el correo del usuario en la sesión.')
    # Si el usuario navega manualmente al login, limpiar mensajes
    if request.GET.get('volver_login') == '1':
        storage = get_messages(request)
        for _ in storage:
            pass
        return redirect('inicio_sesion')
    return render(request, 'inicio/nueva_contraseña.html')