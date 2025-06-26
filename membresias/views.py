from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_GET, require_POST
from membresias import repositorioMembresia as rm

# Create your views here.
def index(request):
    """Vista para administrar membresías"""
    membresias = rm.obtenerMembresias()
    
    context = {
        'membresias': membresias
    }
    
    return render(request, 'membresias/membresias.html', context)

@require_GET
def obtener_membresia(request):
    """Obtener datos de una membresía para editar"""
    membresia_id = request.GET.get('id')
    try:
        membresia = rm.obtenerMembresiaPorId(membresia_id)
        data = {
            'success': True,
            'membresia': {
                'id_membresia': membresia.id_membresia,
                'nombreMembresia': membresia.nombreMembresia,
                'duracionDias': membresia.duracionDias,
                'precio': float(membresia.precio) if membresia.precio else 0
            }
        }
        return JsonResponse(data)
    except rm.obtenerMembresias().model.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Membresía no encontrada'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@require_POST
def guardar_membresia(request):
    """Guardar o actualizar una membresía"""
    membresia_id = request.POST.get('membresia_id')
    nombre = request.POST.get('nombreMembresia')
    duracion = request.POST.get('duracionDias')
    precio = request.POST.get('precio')
    modo_edicion = request.POST.get('modo_edicion') == '1'
    if membresia_id:  # Editar membresía existente
        try:
            membresia = rm.obtenerMembresiaPorId(membresia_id)
            if modo_edicion:
                membresia.precio = float(precio)
            else:
                membresia.nombreMembresia = nombre
                membresia.duracionDias = int(duracion)
                membresia.precio = float(precio)
            membresia.save()
            messages.success(request, f'Membresía "{membresia.nombreMembresia}" actualizada correctamente')
        except rm.obtenerMembresias().model.DoesNotExist:
            messages.error(request, 'Membresía no encontrada')
    else:  # Crear nueva membresía
        membresia = rm.obtenerMembresias().model.objects.create(
            nombreMembresia=nombre,
            duracionDias=int(duracion),
            precio=float(precio)
        )
        messages.success(request, f'Membresía "{nombre}" creada correctamente')
    return redirect('membresias')

@require_POST
def eliminar_membresia(request):
    """Eliminar una membresía"""
    membresia_id = request.POST.get('membresia_id')
    if not membresia_id:
        messages.error(request, 'Error: No se ha especificado el ID de la membresía a eliminar')
        return redirect('membresias')
    try:
        membresia_id = int(membresia_id)
        membresia = rm.obtenerMembresiaPorId(membresia_id)
        nombre = membresia.nombreMembresia
        membresia.delete()
        messages.success(request, f'Membresía "{nombre}" eliminada correctamente')
    except ValueError:
        messages.error(request, 'Error: El ID de la membresía no es válido')
    except rm.obtenerMembresias().model.DoesNotExist:
        messages.error(request, 'Membresía no encontrada')
    return redirect('membresias')