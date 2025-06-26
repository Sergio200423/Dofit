from django.urls import path
from . import views

urlpatterns = [
    path('', views.empleados, name='empleados'),
    path('registrar/', views.registrar_empleado, name='registrar_empleado'),
    path('asistencia/', views.asistencia, name='asistencia'),
    ]