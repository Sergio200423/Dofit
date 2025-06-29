from django.shortcuts import render
from django.http import JsonResponse
import json
from productos import servicioProducto as sp
from productos import repositorioProductos as rp

def productos(request):
    """
    Vista para productos: responde con JSON si es petición AJAX/API, o HTML si es navegación normal.
    """
    productos = sp.prepararVistaProductos()
    tipos = rp.Producto.TIPOS
    estados = rp.Producto.ESTADOS

    # Asegurar que cada producto tenga la lista de estados para el renderizado inicial
    for producto in productos:
        producto['ESTADOS'] = estados

    # Normalizar tipos de productos para conteo robusto
    def normaliza_tipo(valor):
        return valor.strip().lower() if valor else ''

    tipos_validos = {normaliza_tipo(tipo[0]): tipo[0] for tipo in tipos}
    tipo_counts = {tipo[0]: 0 for tipo in tipos}
    tipos_no_validos = []

    for p in productos:
        tipo_prod = normaliza_tipo(p.get('tipo'))
        if tipo_prod in tipos_validos:
            tipo_counts[tipos_validos[tipo_prod]] += 1
        elif tipo_prod in [normaliza_tipo('Barra energética')]:
            tipo_counts['Barra energetica'] += 1
            tipos_no_validos.append(p.get('tipo'))
        else:
            tipos_no_validos.append(p.get('tipo'))

    estado_counts = {value: sum(1 for p in productos if p.get('estado') == value) for value, _ in estados}
    estados_conteo = [(value, label, estado_counts.get(value, 0)) for value, label in estados]

    total_productos = len(productos)
    total_en_stock = estado_counts.get('disponible', 0)
    total_pocas_unidades = estado_counts.get('pocas_unidades', 0)
    total_agotado = estado_counts.get('agotado', 0)

    # Si la petición es AJAX o la URL es /api/productos/, responde JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/productos/'):
        return JsonResponse({
            'productos': productos,
            'tipos': list(tipos),
            'estados': list(estados),
            'estados_conteo': estados_conteo,
            'tipo_counts': tipo_counts,
            'barra_energetica_count': tipo_counts.get('Barra energetica', 0),
            'estado_counts': estado_counts,
            'total_productos': total_productos,
            'total_en_stock': total_en_stock,
            'total_pocas_unidades': total_pocas_unidades,
            'total_agotado': total_agotado,
        })

    # Si no, renderiza la página HTML
    return render(request, 'productos/productos.html', {
        'productos': productos,
        'tipos': tipos,
        'estados': estados,
        'estados_conteo': estados_conteo,
        'tipo_counts': tipo_counts,
        'barra_energetica_count': tipo_counts.get('Barra energetica', 0),
        'estado_counts': estado_counts,
        'total_productos': total_productos,
        'total_en_stock': total_en_stock,
        'total_pocas_unidades': total_pocas_unidades,
        'total_agotado': total_agotado,
    })

def filtrar_producto(request):
    """Filtra productos según los filtros recibidos por AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').lower()
            tipos = data.get('tipo', [])
            estados = data.get('estado', [])

            if isinstance(tipos, str):
                tipos = [tipos] if tipos else []
            if isinstance(estados, str):
                estados = [estados] if estados else []

            productos = sp.prepararVistaProductos()

            # Normalizar tipos para comparación robusta
            def normaliza_tipo(valor):
                return valor.strip().lower() if valor else ''

            tipos_normalizados = set([normaliza_tipo(t) for t in tipos])

            if tipos and 'Todos' not in tipos:
                productos = [p for p in productos if normaliza_tipo(p.get('tipo')) in tipos_normalizados]

            if estados:
                productos = [p for p in productos if p.get('estado') in estados]

            if nombre:
                productos = [p for p in productos if nombre in p.get('nombre_producto', '').lower()]

            # Recalcular contadores de tipo y estado con lógica robusta
            tipos_modelo = rp.Producto.TIPOS
            tipos_validos = {normaliza_tipo(tipo[0]): tipo[0] for tipo in tipos_modelo}
            tipo_counts = {tipo[0]: 0 for tipo in tipos_modelo}

            for p in productos:
                tipo_prod = normaliza_tipo(p.get('tipo'))
                if tipo_prod in tipos_validos:
                    tipo_counts[tipos_validos[tipo_prod]] += 1
                elif tipo_prod in [normaliza_tipo('Barra energética')]:
                    tipo_counts['Barra energetica'] += 1

            barra_energetica_count = tipo_counts.get('Barra energetica', 0)

            # Contadores de estado
            estados_modelo = rp.Producto.ESTADOS
            estado_counts = {value: sum(1 for p in productos if p.get('estado') == value) for value, _ in estados_modelo}
            estados_conteo = [(value, label, estado_counts.get(value, 0)) for value, label in estados_modelo]

            return JsonResponse({
                'productos': productos,
                'tipo_counts': tipo_counts,
                'barra_energetica_count': barra_energetica_count,
                'estado_counts': estado_counts,
                'estados_conteo': estados_conteo,
                'total_productos': len(productos),
                'total_en_stock': estado_counts.get('disponible', 0),
                'total_pocas_unidades': estado_counts.get('pocas_unidades', 0),
                'total_agotado': estado_counts.get('agotado', 0),
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def registrar_producto(request):
    """Registra un nuevo producto vía AJAX"""
    if request.method == 'POST':
        try:
            print('DEBUG registrar_producto: request.content_type =', request.content_type)

            if request.content_type and request.content_type.startswith('multipart/form-data'):
                # Manejo de formulario con imagen
                print('DEBUG registrar_producto: POST keys =', list(request.POST.keys()))
                print('DEBUG registrar_producto: FILES keys =', list(request.FILES.keys()))

                nombre_producto = request.POST.get('nombre_producto')
                precio = request.POST.get('precio')
                cantidad = request.POST.get('existencia')
                descripcion = request.POST.get('descripcion')
                tipo = request.POST.get('tipo')
                fecha_ingreso = request.POST.get('fecha_ingreso')
                imagen = request.FILES.get('imagen')

                print(f"DEBUG registrar_producto: nombre={nombre_producto}, precio={precio}, cantidad={cantidad}, descripcion={descripcion}, tipo={tipo}, fecha_ingreso={fecha_ingreso}, imagen={imagen}")

                valido, mensaje = sp.registrarProducto(
                    nombre_producto=nombre_producto,
                    precio=float(precio) if precio else None,
                    descripcion=descripcion,
                    fecha_ingreso=fecha_ingreso,
                    existencia=int(cantidad) if cantidad else None,
                    tipo=tipo,
                    imagen=imagen
                )

            else:
                print('DEBUG registrar_producto: JSON body')
                data = json.loads(request.body)
                nombre_producto = data.get('nombre_producto')
                precio = data.get('precio')
                cantidad = data.get('existencia')
                descripcion = data.get('descripcion')
                tipo = data.get('tipo')
                fecha_ingreso = data.get('fecha_ingreso')

                print(f"DEBUG registrar_producto: nombre={nombre_producto}, precio={precio}, cantidad={cantidad}, descripcion={descripcion}, tipo={tipo}, fecha_ingreso={fecha_ingreso}")

                valido, mensaje = sp.registrarProducto(
                    nombre_producto=nombre_producto,
                    precio=float(precio) if precio else None,
                    descripcion=descripcion,
                    fecha_ingreso=fecha_ingreso,
                    existencia=int(cantidad) if cantidad else None,
                    tipo=tipo,
                    imagen=None
                )

            if not valido:
                print('DEBUG registrar_producto: registro fallido:', mensaje)
                return JsonResponse({'InformacionValida': False, 'message': mensaje}, status=400)

            print('DEBUG registrar_producto: registro exitoso:', mensaje)
            return JsonResponse({'InformacionValida': True, 'message': mensaje}, status=200)

        except Exception as e:
            print('DEBUG registrar_producto: excepción:', str(e))
            return JsonResponse({'InformacionValida': False, 'message': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_producto(request, producto_id):
    """Obtiene los datos de un producto específico para edición"""
    if request.method == 'GET':
        try:
            producto = rp.obtenerProductoPorId(producto_id)
            if not producto:
                return JsonResponse({'error': 'Producto no encontrado'}, status=404)
            
            return JsonResponse({
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'precio': float(producto.precio),
                'descripcion': producto.descripcion,
                'tipo': producto.tipo,
                'existencia': producto.existencia,
                'estado': producto.estado,
                'fecha_ingreso': producto.fecha_ingreso.strftime('%Y-%m-%d') if producto.fecha_ingreso else '',
                'imagen_url': producto.imagen.url if producto.imagen else None,
            })
        except Exception as e:
            print(f"DEBUG obtener_producto: Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def editar_producto(request, producto_id):
    """Edita un producto existente vía AJAX"""
    if request.method == 'POST':
        try:
            # Manejar formularios con archivos
            nombre_producto = request.POST.get('nombre_producto')
            precio = request.POST.get('precio')
            existencia = request.POST.get('existencia')
            descripcion = request.POST.get('descripcion')
            tipo = request.POST.get('tipo')
            imagen = request.FILES.get('imagen')

            print(f"DEBUG editar_producto: Datos recibidos - nombre={nombre_producto}, precio={precio}, existencia={existencia}, descripcion={descripcion}, tipo={tipo}, imagen={imagen}")

            valido, mensaje = rp.actualizarProducto(
                producto_id=producto_id,
                nombre_producto=nombre_producto,
                precio=float(precio) if precio else None,
                existencia=int(existencia) if existencia else None,
                descripcion=descripcion,
                tipo=tipo,
                imagen=imagen
            )

            if not valido:
                return JsonResponse({'InformacionValida': False, 'message': mensaje}, status=400)

            return JsonResponse({'InformacionValida': True, 'message': mensaje}, status=200)

        except Exception as e:
            print(f"DEBUG editar_producto: Error: {str(e)}")
            return JsonResponse({'InformacionValida': False, 'message': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
