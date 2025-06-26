from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='membresias'),
    path('obtener/', views.obtener_membresia, name='obtener_membresia'),
    path('guardar/', views.guardar_membresia, name='guardar_membresia'),
    path('eliminar/', views.eliminar_membresia, name='eliminar_membresia'),
]