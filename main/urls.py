from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),

    #Clientes
    path('clientes/', views.clientes_view, name='clientes'),
    path('api/clientes/', views.clientes_view, name='obtener_clientes'),
    path('registro_clientes/', views.registro_clientes_view, name='registro_clientes'),
    path('asistencia/', views.asistencia_view, name='asistencia'),
    
    #Productos
    path('productos/', views.productos_view, name='productos'), 
    path('registro_productos/', views.registro_productos_view, name='registro_productos'),
    
    #Pagos
    path('pagos/', views.pagos_view, name='pagos'),
    path('registro_pagos/', views.registro_pagos_view, name='registro_pagos'),
    
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    #Recuperacion de contraseña
    path('recuperar_contraseña/', views.recuperar_contraseña_view, name='recuperar_contraseña'),
    path('correo_enviado/', views.correo_enviado_view, name='email_enviado'),
    path('reenviar_correo/', views.reenviar_correo_view, name='reenviar_correo'),
    path('nueva_contraseña/', views.nueva_contraseña_view, name='nueva_contraseña'),
    
    #Máquinas
    path('maquinas/', views.maquinas_view, name='maquinas'),
]
INSTALLED_APPS = [
    # ... otras aplicaciones ...
    'main',
]