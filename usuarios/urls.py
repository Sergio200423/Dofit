from django.urls import path
from . import views

urlpatterns = [
    # Redirección de /usuarios/ a la lista de usuarios
    path('', views.usuarios, name='usuarios'),
    path('crear/', views.crear_usuario_ajax, name='crear_usuario_ajax'),
    path('eliminar/', views.eliminar_usuario_ajax, name='eliminar_usuario_ajax'),
]