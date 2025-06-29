from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos, name='productos'),
    path('filtrar/', views.filtrar_producto, name='filtrar_producto'),
    path('registrar/', views.registrar_producto, name='registrar_producto'),
    path('obtener/<int:producto_id>/', views.obtener_producto, name='obtener_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
]
