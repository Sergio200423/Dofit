from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('clientes/', views.clientes_view, name='clientes'),
    path('registro_clientes/', views.registro_clientes_view, name='registro_clientes'),
    path('asistencia/', views.asistencia_view, name='asistencia'),
    path('productos/', views.productos_view, name='productos'),
    path('logout/', views.logout_view, name='logout'),
    path('registro_productos/', views.registro_productos_view, name='registro_productos'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('recuperar_contraseña/', views.recuperar_contraseña_view, name='recuperar_contraseña'),
    path('correo_enviado/', views.correo_enviado_view, name='email_enviado'),
    path('nueva_contraseña/', views.nueva_contraseña_view, name='nueva_contraseña')    
]

INSTALLED_APPS = [
    # ... otras aplicaciones ...
    'main',
]