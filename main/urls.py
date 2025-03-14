from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('clientes/', views.clientes_view, name='clientes'),
    path('registro_clientes/', views.registro_clientes_view, name='registro_clientes'),
    path('asistencia/', views.asistencia_view, name='asistencia'),
    path('productos/', views.productos_view, name='productos'),
    path('logout/', views.logout_view, name='logout'),
]

INSTALLED_APPS = [
    # ... otras aplicaciones ...
    'main',
]