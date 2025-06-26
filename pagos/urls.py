from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagos, name='pagos'),
    path('reporte/', views.reporte_pagos, name='reporte_pagos'),
]