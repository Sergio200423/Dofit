from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Rol, Permiso, Usuario, Empleado, Administrador
from .servicio_usuarios import ServicioUsuarios
from .servicio_roles import ServicioRoles
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json


def usuarios(request):
    usuarios = ServicioUsuarios.listar_usuarios()
    roles = ServicioRoles.listar_roles()
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios, 'roles': roles})


def roles(request):
    roles = Rol.objects.all()
    return render(request, 'usuarios/roles.html', {'roles': roles})


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
@require_POST
def crear_rol(request):
    nombre = request.POST.get('nombre', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()
    if not nombre:
        messages.error(request, 'El nombre del rol es obligatorio.')
        return redirect('roles')
    if Rol.objects.filter(nombre=nombre).exists():
        messages.error(request, 'Ya existe un rol con ese nombre.')
        return redirect('roles')
    Rol.objects.create(nombre=nombre, descripcion=descripcion)
    messages.success(request, 'Rol creado exitosamente.')
    return redirect('roles')
