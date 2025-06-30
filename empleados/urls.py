from django.urls import path
from . import views

urlpatterns = [
    path('', views.empleados, name='empleados'),
    path('registrar/', views.registrar_empleado, name='registrar_empleado'),
    path('asistencia/', views.asistencia, name='asistencia'),
    path('asistencia/crear/', views.crear_asistencia_ajax, name='crear_asistencia_ajax'),
    path('asistencia/editar/', views.editar_asistencia_ajax, name='editar_asistencia_ajax'),
    path('asistencia/eliminar/', views.eliminar_asistencia_ajax, name='eliminar_asistencia_ajax'),
    path('asistencia/checkin/', views.checkin_asistencia, name='checkin_asistencia'),
    path('asistencia/checkout/', views.checkout_asistencia, name='checkout_asistencia'),
]