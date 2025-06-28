from django.shortcuts import render
from django.http import JsonResponse
import json
from empleados.servicio_empleados import ServicioEmpleados
from usuarios.models import Usuario, Rol

# Create your views here.
def empleados(request):
    """Vista para empleados: responde con JSON si es petición AJAX/API, o HTML si es navegación normal."""
    servicio = ServicioEmpleados()
    empleados_qs = servicio.listar_empleados().order_by('nombre_empleado')
    # Obtener usuarios con rol empleado
    try:
        rol_empleado = Rol.objects.get(nombre__iexact='empleado')
        usuarios_empleado = Usuario.objects.filter(rol=rol_empleado)
    except Rol.DoesNotExist:
        usuarios_empleado = Usuario.objects.none()
    # Si la petición es AJAX o la URL es /api/empleados/, responde JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/empleados/'):
        empleados_list = [
            {
                'id_empleado': e.id_empleado,
                'nombre_empleado': e.nombre_empleado,
                'turno': e.turno,
                'salario': e.salario,
            }
            for e in empleados_qs
        ]
        return JsonResponse({'empleados': empleados_list})
    # Si no, renderiza la página HTML como antes
    return render(request, 'empleados/empleados.html', {'empleados': empleados_qs, 'usuarios_empleado': usuarios_empleado})

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

            servicio = ServicioEmpleados()
            servicio.crear_empleado(
                nombre_empleado=nombre_empleado,
                turno=turno,
                salario=salario
            )

            # Cambiar clave a InformacionAceptada para sincronizar con JS
            return JsonResponse({
                'InformacionAceptada': True,
                'message': 'Empleado registrado correctamente.'
            })
        except Exception as e:
            return JsonResponse({'InformacionAceptada': False, 'message': f'Error interno: {str(e)}'}, status=500)
    return JsonResponse({'InformacionAceptada': False, 'message': 'Método no permitido'}, status=405)

def asistencia(request):
    return render(request, 'empleados/asistencia.html')