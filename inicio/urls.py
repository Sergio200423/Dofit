from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'), 
    path('login/', views.inicio_sesion, name='inicio_sesion'),
    path('nueva_contrasena/', views.nueva_contrasena, name='nueva_contrasena'),
    path('recuperar_contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('email_enviado/', views.email_enviado, name='email_enviado'),
    path('logout/', views.logout, name='logout'),
    path('reenviar_correo/', views.reenviar_correo, name='reenviar_correo'),
]