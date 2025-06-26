from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.index, name='panel'),
    path('principal/', views.clientes, name='clientes'),
    path('registrar/', views.registrar_cliente, name='registrar_cliente'),
    path('filtrar_cliente/', views.filtrar_cliente, name='filtrar_cliente'),

]