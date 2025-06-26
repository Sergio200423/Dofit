from django.urls import path
from . import views

urlpatterns = [
    path('', views.maquinas, name='maquinas'),
    path('agregar/', views.agregar_maquina, name='agregar_maquina'),
    path('editar/', views.editar_maquina, name='editar_maquina'),
    path('inactivas/', views.maquinas_inactivas_view, name='maquinas_inactivas'),
]
