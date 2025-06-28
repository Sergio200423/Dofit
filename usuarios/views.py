from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Rol, Permiso, Usuario, Empleado, Administrador
from .servicio_usuarios import ServicioUsuarios
from .servicio_roles import ServicioRoles
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json


def usuarios(request):
    usuarios = ServicioUsuarios.listar_usuarios()
    roles = ServicioRoles.listar_roles()
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios, 'roles': roles})


@require_POST
def crear_usuario_ajax(request):
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'success': False, 'error': 'Datos JSON inválidos'})
    usuario = ServicioUsuarios.crear_usuario(data)
    if usuario:
        # Renderizar la fila o card del nuevo usuario para insertar vía JS
        html_usuario = render_to_string('usuarios/fila_usuarios.html', {'usuario': usuario})
        return JsonResponse({'success': True, 'usuario_html': html_usuario})
    return JsonResponse({'success': False, 'error': 'No se pudo crear el usuario'})


@require_POST
def eliminar_usuario_ajax(request):
    try:
        data = json.loads(request.body)
        usuario_id = data.get('usuario_id')
        if not usuario_id:
            return JsonResponse({'success': False, 'error': 'ID de usuario no proporcionado'})
        eliminado = ServicioUsuarios.eliminar_usuario(usuario_id)
        if eliminado:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No se pudo eliminar el usuario'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
