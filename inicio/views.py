from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from inicio.utils.validarLogin import login
from inicio.utils.email import enviar_correo_recuperacion
from django.core.mail import send_mail
from usuarios.models import Usuario
from inicio import GenerarCodigoAleatorio as gca
from django.views.decorators.http import require_http_methods
from inicio.utils.codigo_verificacion import guardar_codigo_verificacion, codigo_verificacion_valido
from inicio.utils.mensajes import limpiar_mensajes
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
        result = login(username, password, n_intentos)
        user = result.get('user')
        n_intentos = result.get('n_intentos', 0)
        if result['success']:
            print(f"[LOGIN DEBUG] Login exitoso para usuario: {user}")
            request.session['usuario_id'] = user.id_usuario
            request.session['usuario_nombre'] = user.nombre_usuario
            request.session['usuario_rol'] = user.rol.nombre
            return redirect('panel')
        else:
            error_msg = result.get('error', 'Error desconocido')
            messages.error(request, error_msg)
            return render(request, 'inicio/login.html', {'n_intentos': n_intentos})
    # Limpiar mensajes antes de mostrar login.html
    limpiar_mensajes(request)
    return render(request, 'inicio/login.html', {'n_intentos': 0})

def recuperar_contrasena(request):
    if request.method == 'POST':
        # Obtener el correo del usuario seleccionado desde el formulario
        correo = request.POST.get('correo')
        intentos_max = 3
        # Validar si el correo ya agotó los intentos antes de enviar el correo
        intentos_dict = request.session.get('intentos_codigo', {})
        intentos_actuales = intentos_dict.get(correo, 0)
        print(f"[DEBUG] intentos_dict en sesión: {intentos_dict}")
        print(f"[DEBUG] intentos_actuales para {correo}: {intentos_actuales}")
        if intentos_actuales >= intentos_max:
            messages.error(request, 'Este correo ya agotó sus intentos. Solicita ayuda o espera un tiempo antes de volver a intentarlo.')
            return redirect('inicio_sesion')
        if correo:
            # Generar código de verificación
            codigo = gca.generar_codigo_verificacion()
            # Guardar en sesión usando util
            guardar_codigo_verificacion(request.session, codigo)
            # Enviar correo
            ok = enviar_correo_recuperacion(correo, codigo)
            if ok is True:
                request.session['correo_usuario'] = correo  # Guardar correo en sesión para el flujo
                return redirect('email_enviado')
            elif isinstance(ok, tuple):
                _, error_msg = ok
                messages.error(request, f'Error al enviar el correo: {error_msg}')
                return redirect('recuperar_contra')
            else:
                messages.error(request, 'Error al enviar el correo')
                return redirect('recuperar_contra')
        else:
            messages.error(request, 'No se seleccionó ningún usuario')
            return redirect('recuperar_contra')
    # GET: mostrar la lista de usuarios
    usuarios = Usuario.objects.all()
    return render(request, 'inicio/recuperar_contra.html', {'usuarios': usuarios})

def reenviar_correo(request):
    # Recuperamos el correo de la sesión
    correo = request.session.get('correo_usuario')
    codigo = request.session.get('codigo_verificacion')

    if correo:
        # Verificar si el código sigue siendo válido
        valido, _ = codigo_verificacion_valido(request.session, codigo)
        if not valido:
            # Generar y guardar un nuevo código si el anterior expiró
            codigo = gca.generar_codigo_verificacion()
            guardar_codigo_verificacion(request.session, codigo)
            messages.info(request, 'El código anterior expiró. Se generó y envió uno nuevo.')
        ok = enviar_correo_recuperacion(correo, codigo)
        if ok is True:
            messages.success(request, 'Correo reenviado correctamente')
        elif isinstance(ok, tuple):
            _, error_msg = ok
            messages.error(request, f'Error al reenviar el correo: {error_msg}')
        else:
            messages.error(request, 'Error al reenviar el correo')
    else:
        messages.error(request, 'No se encontró un correo para reenviar')

    return redirect('email_enviado')

@require_http_methods(["GET", "POST"])
def email_enviado(request):
    limpiar_mensajes(request)
    expired = False
    codigo = request.session.get('codigo_verificacion')
    correo = request.session.get('correo_usuario')
    intentos_max = 3
    intentos_restantes = intentos_max

    if request.method == "POST":
        codigo_ingresado = ''.join([
            request.POST.get('primerNumero', ''),
            request.POST.get('segundoNumero', ''),
            request.POST.get('tercerNumero', ''),
            request.POST.get('cuartoNumero', '')
        ])
        valido, mensaje, intentos_restantes = codigo_verificacion_valido(request.session, codigo_ingresado, intentos_max=intentos_max)
        print(f"[DEBUG] Código ingresado: {codigo_ingresado}")
        print(f"[DEBUG] Resultado validación: {valido}, mensaje: {mensaje}")
        print(f"[DEBUG] POST: {request.POST}")
        if valido and intentos_restantes > 0:
            print("[DEBUG] Código correcto. Redirigiendo a nueva_contraseña.")
            # Asegurarse de que el correo siga en la sesión antes de redirigir
            if not request.session.get('correo_usuario'):
                # Intentar obtener el correo del POST si no está en sesión
                correo_post = request.POST.get('correo')
                if correo_post:
                    request.session['correo_usuario'] = correo_post
                elif correo:
                    request.session['correo_usuario'] = correo
                else:
                    # Si no hay correo, redirigir a recuperar_contra
                    messages.error(request, 'No se encontró el correo en la sesión. Vuelve a iniciar el proceso de recuperación.')
                    return redirect('recuperar_contra')
            return redirect('nueva_contrasena')
        else:
            limpiar_mensajes(request)
            print(f"[DEBUG] {mensaje}")
            if mensaje and 'expirado' in mensaje.lower():
                expired = True
            if mensaje and 'agotado' in mensaje.lower():
                expired = True
            messages.error(request, mensaje)
            return render(request, 'inicio/email_enviado.html', {
                'expired': expired,
                'codigo_verificacion': codigo,
                'intentos_restantes': max(0, intentos_restantes)
            })
    # GET: mostrar intentos restantes
    intentos_dict = request.session.get('intentos_codigo', {})
    intentos_actuales = intentos_dict.get(correo, 0)
    # Si no hay correo en sesión, proteger el flujo
    if not correo:
        messages.error(request, 'No se encontró el correo en la sesión. Vuelve a iniciar el proceso de recuperación.')
        return redirect('recuperar_contrasena')
    return render(request, 'inicio/email_enviado.html', {
        'expired': expired,
        'codigo_verificacion': codigo,
        'intentos_restantes': max(0, intentos_max - intentos_actuales)
    })

def nueva_contrasena(request):
    limpiar_mensajes(request)
    correo_usuario = request.session.get('correo_usuario')
    # Proteger el flujo: si no hay correo en sesión, redirigir
    if not correo_usuario:
        messages.error(request, 'No se encontró el correo en la sesión. Vuelve a iniciar el proceso de recuperación.')
        return redirect('recuperar_contra')
    if request.method == 'POST':
        contra = request.POST.get('contraseña')
        confirmar_contra = request.POST.get('confirmar_contraseña')
        print(f"[DEBUG] Nueva contraseña recibida: {contra}")
        print(f"[DEBUG] Confirmación recibida: {confirmar_contra}")
        print(f"[DEBUG] Correo en sesión: {correo_usuario}")
        if correo_usuario:
            try:
                usuario = Usuario.objects.get(correo=correo_usuario)
                print(f"[DEBUG] Hash actual en BD: {usuario.contra}")
                if check_password(contra, usuario.contra):
                    messages.error(request, 'La nueva contraseña no puede ser igual a la actual.')
                    return render(request, 'inicio/nueva_contraseña.html', {"error_contra_igual": True})
            except Usuario.DoesNotExist:
                messages.error(request, 'No se encontró el usuario para actualizar la contraseña.')
                return render(request, 'inicio/nueva_contraseña.html')
        if contra != confirmar_contra:
            messages.error(request, 'Las contraseñas no coinciden')
        else:
            if correo_usuario:
                try:
                    usuario = Usuario.objects.get(correo=correo_usuario)
                    usuario.contra = make_password(contra)
                    usuario.n_intentos = 0
                    usuario.save()
                    print(f"[DEBUG] Nuevo hash guardado: {usuario.contra}")
                    # Verifica que la contraseña se guarda correctamente
                    if check_password(contra, usuario.contra):
                        print("[DEBUG] El hash coincide con la nueva contraseña.")
                    else:
                        print("[DEBUG] El hash NO coincide con la nueva contraseña.")
                    # Cierra todas las sesiones activas del usuario (si aplica)
                    sessions = Session.objects.all()
                    for session in sessions:
                        data = session.get_decoded()
                        if data.get('usuario_id') == usuario.id_usuario:
                            session.delete()
                    # Limpiar mensajes antes de redirigir al login
                    limpiar_mensajes(request)
                    messages.success(request, 'Contraseña actualizada correctamente. Todas las sesiones han sido cerradas.')
                    # Limpiar correo de la sesión tras éxito
                    if 'correo_usuario' in request.session:
                        del request.session['correo_usuario']
                    return redirect('inicio_sesion')
                except Usuario.DoesNotExist:
                    messages.error(request, 'No se encontró el usuario para actualizar la contraseña.')
            else:
                messages.error(request, 'No se encontró el correo del usuario en la sesión.')
    # Si el usuario navega manualmente al login, limpiar mensajes
    if request.GET.get('volver_login') == '1':
        limpiar_mensajes(request)
        return redirect('inicio_sesion')
    return render(request, 'inicio/nueva_contraseña.html')

def logout(request):
    """Cierra la sesión del usuario y lo redirige al login."""
    # También limpiamos cualquier variable personalizada de sesión
    request.session.flush()
    messages.success(request, 'Cierre de sesión exitoso.')
    return redirect('inicio_sesion')