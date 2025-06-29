from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagos, name='pagos'),
    path('realizar_pago/', views.realizar_pago, name='realizar_pago'),
    path('api/productos/', views.api_productos, name='api_productos'),
    path('api/membresias/', views.api_membresias, name='api_membresias'),
    path('reporte/', views.reporte_pagos, name='reporte_pagos'),
]
