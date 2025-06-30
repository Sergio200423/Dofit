from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count, Avg
import json
from datetime import datetime, date
import calendar
from productos import repositorioProductos as rp
from membresias import repositorioMembresia as rm
from pagos import repositorioPago as rpago
from pagos import repositorioPagoProductos as rpp
from pagos import servicioPagos as sp
from main.models import Pago, PagoProducto

def pagos(request):
    """Vista principal del sistema de pagos"""
    if request.GET.get('success') == '1':
        return render(request, 'pagos/pagos.html', {'success_message': '¡Compra realizada con éxito!'})
    return render(request, 'pagos/pagos.html')

@csrf_exempt
@require_http_methods(["POST"])
def realizar_pago(request):
    """API endpoint para procesar pagos - CORREGIDO"""
    try:
        data = json.loads(request.body)
        productos = data.get('productos', [])
        membresias = data.get('membresias', [])
        descuento_porcentaje = data.get('descuento', 0)
        
        # Validar que hay items en el carrito
        if not productos and not membresias:
            return JsonResponse({
                'success': False,
                'error': 'El carrito está vacío'
            })
        
        # Calcular totales
        total_productos = 0
        total_membresias = 0
        
        # Validar y calcular productos
        productos_validados = []
        for item in productos:
            producto = rp.obtenerProductoPorId(item['id'])
            if not producto:
                return JsonResponse({
                    'success': False,
                    'error': f'Producto con ID {item["id"]} no encontrado'
                })
            
            if producto.existencia < item['quantity']:
                return JsonResponse({
                    'success': False,
                    'error': f'Stock insuficiente para {producto.nombre_producto}'
                })
            
            total_productos += producto.precio * item['quantity']
            productos_validados.append({
                'producto': producto,
                'cantidad': item['quantity']
            })
        
        # Validar y calcular membresías
        membresias_validadas = []
        for item in membresias:
            membresia = rm.obtenerMembresiaPorId(item['id'])
            if not membresia:
                return JsonResponse({
                    'success': False,
                    'error': f'Membresía con ID {item["id"]} no encontrada'
                })
            
            total_membresias += membresia.precio * item['quantity']
            membresias_validadas.append({
                'membresia': membresia,
                'cantidad': item['quantity']
            })
        
        # Calcular total con descuento
        subtotal = total_productos + total_membresias
        descuento_monto = (subtotal * descuento_porcentaje) / 100
        total_final = subtotal - descuento_monto
        
        # SOLUCIÓN CORREGIDA: Usar los nombres de campo correctos
        from main.models import Cliente, Pago
        
        # Buscar o crear cliente para ventas directas con los campos correctos
        cliente_venta_directa, created = Cliente.objects.get_or_create(
            nombre_cliente='VENTA DIRECTA',  # Corregido: usar nombre_cliente
            defaults={
                'empleado_id': 1,  # Asignar un empleado por defecto (ajusta según tu DB)
                'fecha_nacimiento': date(1990, 1, 1),  # Fecha por defecto
                'fecha_registro': date.today(),
                'sexo': 'O'  # Otro/No especificado
            }
        )
        
        # Crear el pago con el cliente de venta directa
        tipo_pago = []
        if productos_validados:
            tipo_pago.append('Producto')
        if membresias_validadas:
            tipo_pago.append('Membresia')
        
        # Crear pago usando el modelo directamente
        pago = Pago.objects.create(
            tipo=' + '.join(tipo_pago),
            fecha=date.today(),
            cliente=cliente_venta_directa,
            total_a_pagar=total_final
        )
        
        # Registrar productos en el pago
        for item in productos_validados:
            producto = item['producto']
            cantidad = item['cantidad']
            
            # Crear registro de pago-producto
            rpp.crearPagoProducto(
                pago=pago,
                producto=producto,
                fecha_pago=date.today(),
                cantidad=cantidad
            )
            
            # Actualizar stock
            nuevo_stock = producto.existencia - cantidad
            producto.existencia = nuevo_stock
            producto.save()
        
        # Registrar membresías (si las tienes en tu modelo de pagos)
        # Por ahora solo registramos la venta
        
        return JsonResponse({
            'success': True,
            'pago_id': pago.id_pago,
            'total': float(total_final),
            'message': 'Pago procesado exitosamente'
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error completo en realizar_pago: {error_details}")
        return JsonResponse({
            'success': False,
            'error': f'Error al procesar el pago: {str(e)}'
        })

def api_productos(request):
    """API para obtener productos"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        productos = rp.obtenerProductos()
        productos_data = []
        
        for producto in productos:
            productos_data.append({
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'precio': float(producto.precio),
                'descripcion': producto.descripcion,
                'existencia': producto.existencia,
                'tipo': producto.tipo,
                'imagen': producto.imagen.url if producto.imagen else None,
            })
        
        return JsonResponse({'productos': productos_data})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def api_membresias(request):
    """API para obtener membresías"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        membresias = rm.obtenerMembresias()
        membresias_data = []
        
        for membresia in membresias:
            membresias_data.append({
                'id_membresia': membresia.id_membresia,
                'nombreMembresia': membresia.nombreMembresia,
                'precio': float(membresia.precio),
                'duracionDias': membresia.duracionDias,
            })
        
        return JsonResponse({'membresias': membresias_data})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def reporte_pagos(request):
    """Vista del reporte de pagos con totales, promedios y datos para gráficos"""
    pagos_qs = rpago.obtenerPagos().order_by('-fecha')
    pagos_context = []
    total_membresias = 0
    count_membresias = 0
    total_productos_pagos = 0
    count_productos = 0
    total_descuentos = 0
    count_descuentos = 0
    total_general = 0
    total_pagos_count = pagos_qs.count()
    sum_membresias = []
    sum_productos = []
    meses = [calendar.month_name[i] for i in range(1, 13)]
    mensual_membresias = [0]*12
    mensual_productos = [0]*12
    for pago in pagos_qs:
        productos = rpp.obtenerPagoProductosPorPago(pago)
        productos_list = [
            {
                'nombre': p.producto.nombre_producto,
                'cantidad': p.cantidad,
                'precio': p.producto.precio,
                'total': p.producto.precio * p.cantidad
            } for p in productos
        ]
        # Sumar totales y contar tipos
        if 'Membresia' in pago.tipo:
            total_membresias += pago.total_a_pagar
            count_membresias += 1
            sum_membresias.append(pago.total_a_pagar)
            mensual_membresias[pago.fecha.month-1] += pago.total_a_pagar
        if 'Producto' in pago.tipo:
            total_productos_pagos += pago.total_a_pagar
            count_productos += 1
            sum_productos.append(pago.total_a_pagar)
            mensual_productos[pago.fecha.month-1] += pago.total_a_pagar
        total_general += pago.total_a_pagar
        pagos_context.append({
            'id_pago': pago.id_pago,
            'tipo': pago.tipo,
            'fecha': pago.fecha,
            'total_final': pago.total_a_pagar,
            'total_original': pago.total_a_pagar,  # Ajusta si tienes descuentos
            'cliente': pago.cliente.nombre_cliente if pago.cliente else 'N/A',
            'productos': productos_list,
            'descuentos': [],  # Agrega si tienes descuentos
            'total_descuentos': 0,  # Ajusta si tienes descuentos
        })
    # Promedios
    promedio_membresias = sum(sum_membresias)/count_membresias if count_membresias else 0
    promedio_productos = sum(sum_productos)/count_productos if count_productos else 0
    # Mes más activo
    mes_mas_activo_idx = (mensual_membresias + mensual_productos).index(max(mensual_membresias + mensual_productos)) if total_pagos_count else 0
    mes_mas_activo = meses[mes_mas_activo_idx] if total_pagos_count else ''
    # Datos para gráficos
    datos_membresias = json.dumps({
        'labels': meses,
        'data': mensual_membresias
    })
    datos_productos = json.dumps({
        'labels': meses,
        'data': mensual_productos
    })
    datos_mensuales = json.dumps({
        'labels': meses,
        'membresias': mensual_membresias,
        'productos': mensual_productos
    })
    historial_anual_labels = json.dumps(meses)
    historial_anual_data = json.dumps([mensual_membresias[i] + mensual_productos[i] for i in range(12)])
    context = {
        'pagos': pagos_context,
        'total_membresias': total_membresias,
        'count_membresias': count_membresias,
        'total_productos_pagos': total_productos_pagos,
        'count_productos': count_productos,
        'total_descuentos': total_descuentos,
        'count_descuentos': count_descuentos,
        'total_general': total_general,
        'total_pagos_count': total_pagos_count,
        'promedio_membresias': promedio_membresias,
        'promedio_productos': promedio_productos,
        'mes_mas_activo': mes_mas_activo,
        'datos_membresias': datos_membresias,
        'datos_productos': datos_productos,
        'datos_mensuales': datos_mensuales,
        'historial_anual_labels': historial_anual_labels,
        'historial_anual_data': historial_anual_data,
    }
    return render(request, 'pagos/reporte_pagos.html', context)
