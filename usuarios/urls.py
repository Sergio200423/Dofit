from django.urls import path
from . import views

urlpatterns = [
    # Redirección de /usuarios/ a la lista de usuarios
    path('', views.usuario_list, name='usuario_list'),
    # Rol
    path('roles/', views.rol_list, name='rol_list'),
    path('roles/nuevo/', views.rol_create, name='rol_create'),
    path('roles/editar/<int:pk>/', views.rol_update, name='rol_update'),
    path('roles/eliminar/<int:pk>/', views.rol_delete, name='rol_delete'),
    # Permiso
    path('permisos/', views.permiso_list, name='permiso_list'),
    path('permisos/nuevo/', views.permiso_create, name='permiso_create'),
    path('permisos/editar/<int:pk>/', views.permiso_update, name='permiso_update'),
    path('permisos/eliminar/<int:pk>/', views.permiso_delete, name='permiso_delete'),
    # Usuario
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/nuevo/', views.usuario_create, name='usuario_create'),
    path('usuarios/editar/<int:pk>/', views.usuario_update, name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', views.usuario_delete, name='usuario_delete'),
    # Empleado
    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/nuevo/', views.empleado_create, name='empleado_create'),
    path('empleados/editar/<int:pk>/', views.empleado_update, name='empleado_update'),
    path('empleados/eliminar/<int:pk>/', views.empleado_delete, name='empleado_delete'),
    # Administrador
    path('administradores/', views.administrador_list, name='administrador_list'),
    path('administradores/nuevo/', views.administrador_create, name='administrador_create'),
    path('administradores/editar/<int:pk>/', views.administrador_update, name='administrador_update'),
    path('administradores/eliminar/<int:pk>/', views.administrador_delete, name='administrador_delete'),
]
