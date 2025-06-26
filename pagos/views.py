from django.shortcuts import render
from django.contrib import messages
import json
from collections import defaultdict
from pagos import repositorioPago as rpa
from pagos import repositorioPagoDescuento as rpd
from pagos import repositorioPagoProductos as rpp

# Create your views here.
def pagos(request):
    # Si viene ?success=1 en la URL, mostrar mensaje de éxito
    if request.GET.get('success') == '1':
        messages.success(request, '¡Compra realizada con éxito!')
    return render(request, 'pagos/pagos.html')

def reporte_pagos(request):
    pagos = rpa.obtenerPagos().order_by('-fecha')
    pagos_context = []
    total_pagos = 0
    total_descuentos = 0
    total_productos = 0
    total_final = 0
    historial_fechas = []
    historial_totales = []
    pagos_semanal = defaultdict(float)
    pagos_mensual = defaultdict(float)
    pagos_anual = defaultdict(float)
    for pago in pagos:
        descuentos = rpd.obtenerDescuentosPorPago(pago)
        productos = rpp.obtenerPagoProductosPorPago(pago)
        suma_descuentos = sum([d.descuento.monto for d in descuentos])
        suma_productos = sum([p.cantidad for p in productos])
        total_pagos += pago.total_a_pagar
        total_descuentos += suma_descuentos
        total_productos += suma_productos
        total_final += pago.total_a_pagar - suma_descuentos
        historial_fechas.append(pago.fecha.strftime('%Y-%m-%d'))
        historial_totales.append(float(pago.total_a_pagar))
        year, week, _ = pago.fecha.isocalendar()
        pagos_semanal[f"{year}-S{week:02d}"] += float(pago.total_a_pagar)
        pagos_mensual[pago.fecha.strftime('%Y-%m')] += float(pago.total_a_pagar)
        pagos_anual[str(pago.fecha.year)] += float(pago.total_a_pagar)
        pagos_context.append({
            'id': pago.id_pago,
            'tipo': pago.tipo,
            'fecha': pago.fecha.strftime('%d/%m/%Y'),  # <-- Formato dd/mm/yyyy para mostrar en el template
            'cliente': pago.cliente.nombre_cliente if pago.cliente else '',
            'total_original': pago.total_a_pagar,
            'total_final': pago.total_a_pagar - suma_descuentos,
            'descuentos': [
                {
                    'nombre': d.descuento.nombre,
                    'monto': d.descuento.monto,
                    'descripcion': d.descuento.descripcion
                } for d in descuentos
            ],
            'productos': [
                {
                    'nombre': p.producto.nombre_producto,
                    'cantidad': p.cantidad,
                    'precio': p.producto.precio,
                    'total': p.total_a_pagar()
                } for p in productos
            ]
        })
    semanal_labels = sorted(pagos_semanal.keys())
    mensual_labels = sorted(pagos_mensual.keys())
    anual_labels = sorted(pagos_anual.keys())
    context = {
        # Pass pagos_context as a Python list for template iteration
        'pagos': pagos_context,
        # Only serialize to JSON the variables needed for JS
        'total_pagos': json.dumps(total_pagos),
        'total_descuentos': json.dumps(total_descuentos),
        'total_productos': json.dumps(total_productos),
        'total_final': json.dumps(total_final),
        'historial_fechas': json.dumps(historial_fechas[::-1]),
        'historial_totales': json.dumps(historial_totales[::-1]),
        'historial_semanal_labels': json.dumps(semanal_labels),
        'historial_semanal_data': json.dumps([pagos_semanal[k] for k in semanal_labels]),
        'historial_mensual_labels': json.dumps(mensual_labels),
        'historial_mensual_data': json.dumps([pagos_mensual[k] for k in mensual_labels]),
        'historial_anual_labels': json.dumps(anual_labels),
        'historial_anual_data': json.dumps([pagos_anual[k] for k in anual_labels]),
    }
    return render(request, 'pagos/reportePagos.html', context)
