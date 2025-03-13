from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
]

INSTALLED_APPS = [
    # ... otras aplicaciones ...
    'main',
]