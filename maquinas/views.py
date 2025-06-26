from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from main.models import Maquina
import json
from django.contrib import messages

# Create your views here.
def maquinas(request):
    # Obtener todas las máquinas
    maquinas = Maquina.objects.all()
    
    # Convertir las máquinas a formato JSON para usar en JavaScript
    maquinas_json = json.dumps([{
        'id_maquina': maquina.id_maquina,
        'nombre': maquina.nombre,
        'cantidad': maquina.cantidad,
        'estado': maquina.estado,
        'descripcion': maquina.descripcion,
        'razon_inactividad': maquina.razon_inactividad,
        'fecha_inactividad': maquina.fecha_inactividad.strftime('%Y-%m-%d') if maquina.fecha_inactividad else None,
        'notas_inactividad': maquina.notas_inactividad,
        'fecha_estimada_reparacion': maquina.fecha_estimada_reparacion.strftime('%Y-%m-%d') if maquina.fecha_estimada_reparacion else None,
        'imagen_url': request.build_absolute_uri(maquina.imagen.url) if maquina.imagen else None
    } for maquina in maquinas])
    
    # Obtener máquinas en reparación o mal estado
    maquinas_inactivas = Maquina.objects.filter(estado='inactiva')
    
    context = {
        'maquinas': maquinas,
        'maquinas_json': maquinas_json,
        'maquinas_inactivas': maquinas_inactivas
    }
    
    return render(request, 'maquinas/maquinas.html', context)

def editar_maquina(request):
    if request.method == 'POST':
        maquina_id = request.POST.get('maquina_id')
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        estado = request.POST.get('estado')
        descripcion = request.POST.get('descripcion')
        
        # Buscar la máquina por ID
        maquina = get_object_or_404(Maquina, id_maquina=maquina_id)
        
        # Actualizar los campos básicos
        maquina.nombre = nombre
        maquina.cantidad = int(cantidad)
        maquina.descripcion = descripcion
        
        # Manejar el cambio de estado
        estado_anterior = maquina.estado
        maquina.estado = estado
        
        # Si la máquina pasa de activa a inactiva, registrar información adicional
        if estado_anterior == 'activa' and estado == 'inactiva':
            razon_inactividad = request.POST.get('razon_inactividad')
            notas_inactividad = request.POST.get('notas_inactividad')
            fecha_estimada = request.POST.get('fecha_estimada_reparacion')
            
            maquina.razon_inactividad = razon_inactividad
            maquina.notas_inactividad = notas_inactividad
            maquina.fecha_inactividad = date.today()
            
            if fecha_estimada:
                maquina.fecha_estimada_reparacion = fecha_estimada
        
        # Si la máquina pasa de inactiva a activa, resetear los campos de inactividad
        elif estado_anterior == 'inactiva' and estado == 'activa':
            maquina.razon_inactividad = 'no_aplica'
            maquina.notas_inactividad = None
            maquina.fecha_inactividad = None
            maquina.fecha_estimada_reparacion = None
        
        # Manejar la imagen si se proporciona una nueva
        if 'imagen' in request.FILES:
            maquina.imagen = request.FILES['imagen']
        
        # Guardar los cambios
        maquina.save()
        
        messages.success(request, f'Máquina "{nombre}" actualizada correctamente')
        return redirect('maquinas')
    
    # Si no es POST, redirigir a la página de máquinas
    return redirect('maquinas')

def agregar_maquina(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        estado = request.POST.get('estado')
        descripcion = request.POST.get('descripcion')
        
        # Crear nueva máquina
        maquina = Maquina(
            nombre=nombre,
            cantidad=int(cantidad),
            estado=estado,
            descripcion=descripcion
        )
        
        # Si la máquina es inactiva, registrar información adicional
        if estado == 'inactiva':
            razon_inactividad = request.POST.get('razon_inactividad')
            notas_inactividad = request.POST.get('notas_inactividad')
            fecha_estimada = request.POST.get('fecha_estimada_reparacion')
            
            maquina.razon_inactividad = razon_inactividad
            maquina.notas_inactividad = notas_inactividad
            maquina.fecha_inactividad = date.today()
            
            if fecha_estimada:
                maquina.fecha_estimada_reparacion = fecha_estimada
        
        # Manejar la imagen si se proporciona
        if 'imagen' in request.FILES:
            maquina.imagen = request.FILES['imagen']
        
        # Guardar la máquina
        maquina.save()
        
        messages.success(request, f'Máquina "{nombre}" agregada correctamente')
        return redirect('maquinas')
    
    # Si es GET, mostrar el formulario para agregar
    return render(request, 'maquinas/modal_agregar_maquina.html')

def maquinas_inactivas_view(request):
    # Obtener máquinas inactivas
    maquinas_inactivas = Maquina.objects.filter(estado='inactiva')
    
    context = {
        'maquinas_inactivas': maquinas_inactivas
    }
    
    return render(request, 'maquinas/maquinas_inactivas.html', context)