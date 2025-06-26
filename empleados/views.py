from django.shortcuts import render
from usuarios.models import Empleado
from django.http import JsonResponse
import json

# Create your views here.
def empleados(request):
    """Vista para empleados: responde con JSON si es petición AJAX/API, o HTML si es navegación normal."""
    empleados = Empleado.objects.all().order_by('nombre_empleado')
    # Si la petición es AJAX o la URL es /api/empleados/, responde JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/empleados/'):
        empleados_list = [
            {
                'id_empleado': e.id_empleado,
                'nombre_empleado': e.nombre_empleado,
                'turno': e.turno,
                'salario': e.salario,
            }
            for e in empleados
        ]
        return JsonResponse({'empleados': empleados_list})
    # Si no, renderiza la página HTML como antes
    return render(request, 'empleados/empleados.html', {'empleados': empleados})

def registrar_empleado(request):
    """
    Vista para registrar un nuevo empleado vía AJAX (POST JSON o form-data).
    Retorna JSON siempre que la petición sea AJAX.
    """
    if request.method == 'POST':
        try:
            # Soportar tanto JSON como form-data
            if request.content_type.startswith('application/json'):
                data = json.loads(request.body)
            else:
                data = request.POST

            nombre_empleado = data.get('nombre_empleado')
            turno = data.get('turno')
            salario = data.get('salario')

            # Validación básica
            if not all([nombre_empleado, turno, salario]):
                return JsonResponse({
                    'success': False,
                    'message': 'Todos los campos obligatorios deben estar completos.'
                }, status=400)

            Empleado.objects.create(
                nombre_empleado=nombre_empleado,
                turno=turno,
                salario=salario
            )

            return JsonResponse({
                'success': True,
                'message': 'Empleado registrado correctamente.'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

def asistencia(request):
    return render(request, 'empleados/asistencia.html')