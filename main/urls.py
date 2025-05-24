from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('inicio/', views.inicio_view, name="inicio"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #Clientes
    path('clientes/', views.clientes_view, name='clientes'),
    path('api/clientes/', views.clientes_view, name='obtener_clientes'),
    path('clientes/registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('clientes/editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/filtrar_cliente/', views.filtrar_cliente, name='filtrar_cliente'),    
    path('registro_clientes/', views.registro_clientes_view, name='registro_clientes'),
    path('asistencia/', views.asistencia_view, name='asistencia'),
    
    #Productos
    path('productos/', views.productos_view, name='productos'), 
    path('api/productos/', views.productos_view, name='obtener_productos'),
    path('productos/filtrar_producto/', views.filtrar_producto, name='filtrar_producto'),
    path('productos/registrar_producto/', views.registrar_producto, name='registrar_producto'),
    path('productos/editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('registro_productos/', views.registro_productos_view, name='registro_productos'),
    
    #Pagos
    path('pagos/', views.pagos_view, name='pagos'),
    path('registro_pagos/', views.registro_pagos_view, name='registro_pagos'),
    path('reportePago/', views.reportePago_view, name='reportePago'),
    path('api/realizar_pago/', views.realizar_pago_api, name='realizar_pago_api'),
    
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    #Recuperacion de contraseña
    path('recuperar_contraseña/', views.recuperar_contraseña_view, name='recuperar_contraseña'),
    path('correo_enviado/', views.correo_enviado_view, name='email_enviado'),
    path('reenviar_correo/', views.reenviar_correo_view, name='reenviar_correo'),
    path('nueva_contraseña/', views.nueva_contraseña_view, name='nueva_contraseña'),

    #Máquinas
    path('maquinas/', views.maquinas_view, name='maquinas'),
    path('maquinas/agregar/', views.agregar_maquina, name='agregar_maquina'),
    path('maquinas/editar/', views.editar_maquina, name='editar_maquina'),
    path('maquinas/inactivas/', views.maquinas_inactivas_view, name='maquinas_inactivas'),

    #Membresias
    path('membresias/', views.membresias_view, name='membresias'),
    path('membresias/obtener/', views.obtener_membresia, name='obtener_membresia'),
    path('membresias/guardar/', views.guardar_membresia, name='guardar_membresia'),
    path('membresias/eliminar/', views.eliminar_membresia, name='eliminar_membresia'),
    path('api/tipo_membresias/', views.api_tipo_membresias, name='api_tipo_membresias'),

    path('dashboard_empleado/', views.dashboard_empleado, name='dashboard_empleado'),

        # Empleados
    path('empleados/', views.empleados_view, name='empleados'),

    

]
INSTALLED_APPS = [
    # ... otras aplicaciones ...
    'main',
]