from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime, date
from productos import repositorioProductos as rp
from membresias import repositorioMembresia as rm
from pagos import repositorioPago as rpago
from pagos import repositorioPagoProductos as rpp
from pagos import servicioPagos as sp

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
    """Vista del reporte de pagos"""
    pagos = rpago.obtenerPagos().order_by('-fecha')
    pagos_context = []
    
    for pago in pagos:
        productos = rpp.obtenerPagoProductosPorPago(pago)
        
        pagos_context.append({
            'id': pago.id_pago,
            'tipo': pago.tipo,
            'fecha': pago.fecha.strftime('%d/%m/%Y'),
            'total': pago.total_a_pagar,
            'cliente': pago.cliente.nombre_cliente if pago.cliente else 'N/A',  # Corregido
            'productos': [
                {
                    'nombre': p.producto.nombre_producto,
                    'cantidad': p.cantidad,
                    'precio': p.producto.precio,
                    'total': p.producto.precio * p.cantidad
                } for p in productos
            ]
        })
    
    context = {
        'pagos': pagos_context,
        'total_ventas': sum(p.total_a_pagar for p in pagos),
        'total_transacciones': len(pagos)
    }
    
    return render(request, 'pagos/reportePagos.html', context)
