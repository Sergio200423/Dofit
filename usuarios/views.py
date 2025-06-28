from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Rol, Permiso, Usuario, Empleado, Administrador
from .forms import RolForm, PermisoForm, UsuarioForm, EmpleadoForm, AdministradorForm

# --- ROL CRUD ---
def rol_list(request):
    roles = Rol.objects.all()
    return render(request, 'usuarios/rol_list.html', {'roles': roles})

def rol_create(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rol_list')
    else:
        form = RolForm()
    return render(request, 'usuarios/rol_form.html', {'form': form})

def rol_update(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('rol_list')
    else:
        form = RolForm(instance=rol)
    return render(request, 'usuarios/rol_form.html', {'form': form})

def rol_delete(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        rol.delete()
        return redirect('rol_list')
    return render(request, 'usuarios/rol_confirm_delete.html', {'rol': rol})

# --- PERMISO CRUD ---
def permiso_list(request):
    permisos = Permiso.objects.all()
    return render(request, 'usuarios/permiso_list.html', {'permisos': permisos})

def permiso_create(request):
    if request.method == 'POST':
        form = PermisoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('permiso_list')
    else:
        form = PermisoForm()
    return render(request, 'usuarios/permiso_form.html', {'form': form})

def permiso_update(request, pk):
    permiso = get_object_or_404(Permiso, pk=pk)
    if request.method == 'POST':
        form = PermisoForm(request.POST, instance=permiso)
        if form.is_valid():
            form.save()
            return redirect('permiso_list')
    else:
        form = PermisoForm(instance=permiso)
    return render(request, 'usuarios/permiso_form.html', {'form': form})

def permiso_delete(request, pk):
    permiso = get_object_or_404(Permiso, pk=pk)
    if request.method == 'POST':
        permiso.delete()
        return redirect('permiso_list')
    return render(request, 'usuarios/permiso_confirm_delete.html', {'permiso': permiso})

# --- USUARIO CRUD ---
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})

def usuario_create(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                html = render_to_string('usuarios/_usuario_form_fields.html', {'form': form}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
        else:
            form = UsuarioForm()
            html = render_to_string('usuarios/_usuario_form_fields.html', {'form': form}, request=request)
            return JsonResponse({'form_html': html})
    else:
        # Si no es AJAX, solo renderiza el fragmento para pruebas manuales (no redirect)
        form = UsuarioForm()
        return render(request, 'usuarios/_usuario_form_fields.html', {'form': form})


def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            form = UsuarioForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                html = render_to_string('usuarios/_usuario_form_fields.html', {'form': form}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
        else:
            form = UsuarioForm(instance=usuario)
            html = render_to_string('usuarios/_usuario_form_fields.html', {'form': form}, request=request)
            return JsonResponse({'form_html': html})
    else:
        # Si no es AJAX, solo renderiza el fragmento para pruebas manuales (no redirect)
        form = UsuarioForm(instance=usuario)
        return render(request, 'usuarios/_usuario_form_fields.html', {'form': form})

def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('usuario_list')
    # Para GET, solo mostrar el nombre en el modal (el modal ya lo hace con JS)
    return JsonResponse({'success': False})

# --- EMPLEADO CRUD ---
def empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'usuarios/empleado_list.html', {'empleados': empleados})

def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'usuarios/empleado_form.html', {'form': form})

def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'usuarios/empleado_form.html', {'form': form})

def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleado_list')
    return render(request, 'usuarios/empleado_confirm_delete.html', {'empleado': empleado})

# --- ADMINISTRADOR CRUD ---
def administrador_list(request):
    administradores = Administrador.objects.all()
    return render(request, 'usuarios/administrador_list.html', {'administradores': administradores})

def administrador_create(request):
    if request.method == 'POST':
        form = AdministradorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrador_list')
    else:
        form = AdministradorForm()
    return render(request, 'usuarios/administrador_form.html', {'form': form})

def administrador_update(request, pk):
    administrador = get_object_or_404(Administrador, pk=pk)
    if request.method == 'POST':
        form = AdministradorForm(request.POST, instance=administrador)
        if form.is_valid():
            form.save()
            return redirect('administrador_list')
    else:
        form = AdministradorForm(instance=administrador)
    return render(request, 'usuarios/administrador_form.html', {'form': form})

def administrador_delete(request, pk):
    administrador = get_object_or_404(Administrador, pk=pk)
    if request.method == 'POST':
        administrador.delete()
        return redirect('administrador_list')
    return render(request, 'usuarios/administrador_confirm_delete.html', {'administrador': administrador})
