from django.urls import path
from . import views

urlpatterns = [
    path('', views.backup, name='backup'),
    path('backup-json/', views.backup_json, name='backup_json'),
    path('restore-json/', views.restore_json, name='restore_json'),
    path('backup-history/', views.backup_history, name='backup_history'),
    path('delete-backups/', views.delete_backups, name='delete_backups'),
]