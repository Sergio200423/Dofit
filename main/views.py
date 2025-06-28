# DJANGO IMPORTS
from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os
import sys
from django.db import connections
from .backup_utils import get_next_backup_filename, delete_all_backups
from .backup_list_utils import list_backups
import json
from django.views.decorators.http import require_POST

def backup(request):
    return render(request, 'main/backup.html')


def backup_json(request):
    """
    Genera un backup de todos los modelos en formato JSON usando dumpdata, lo guarda en 'backups/' y lo descarga.
    """
    for conn in connections.all():
        conn.close()
    backups_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backups_dir, exist_ok=True)
    filename = get_next_backup_filename(backups_dir)
    backup_path = os.path.join(backups_dir, filename)
    # Ejecutar dumpdata para todos los modelos
    result = subprocess.run([
        sys.executable, 'manage.py', 'dumpdata',
        '--natural-foreign', '--natural-primary', '--indent', '2'
    ], capture_output=True, text=True)
    if result.returncode != 0:
        return HttpResponse(f'Error al generar backup: {result.stderr}', status=500)
    # Guardar el resultado en el archivo
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(result.stdout)
    # Devolver el archivo como descarga
    with open(backup_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

@csrf_exempt  # Quitar si luego agregas protección CSRF y autenticación
def restore_json(request):
    if request.method == 'POST':
        # Restaurar desde archivo subido
        if request.FILES.get('backup_file'):
            backup_file = request.FILES['backup_file']
            temp_path = os.path.join(settings.BASE_DIR, 'temp_restore.json')
            with open(temp_path, 'wb+') as destination:
                for chunk in backup_file.chunks():
                    destination.write(chunk)
            restore_path = temp_path
            remove_temp = True
        else:
            # Restaurar desde nombre de backup (AJAX)
            try:
                data = json.loads(request.body.decode('utf-8'))
                backup_name = data.get('backup_name')
            except Exception:
                backup_name = None
            if backup_name:
                backups_dir = os.path.join(settings.BASE_DIR, 'backups')
                restore_path = os.path.join(backups_dir, backup_name)
                if not os.path.exists(restore_path):
                    return HttpResponse('Backup no encontrado', status=404)
                remove_temp = False
            else:
                return HttpResponse('No se recibió archivo ni nombre de backup', status=400)
        # Ejecutar loaddata
        result = subprocess.run([
            sys.executable, 'manage.py', 'loaddata', restore_path
        ], capture_output=True, text=True)
        if 'remove_temp' in locals() and remove_temp:
            os.remove(restore_path)
        if result.returncode == 0:
            return HttpResponse('Restauración exitosa')
        else:
            return HttpResponse(f'Error al restaurar: {result.stderr}', status=500)
    return HttpResponse('Método no permitido', status=405)

def backup_history(request):
    """
    Devuelve la lista de backups disponibles en formato JSON, incluyendo el total de espacio usado.
    """
    data = list_backups()
    return HttpResponse(
        json.dumps(data),
        content_type='application/json'
    )

@require_POST
@csrf_exempt
def delete_backups(request):
    backups_dir = os.path.join(settings.BASE_DIR, 'backups')
    count = delete_all_backups(backups_dir)
    return HttpResponse(json.dumps({'deleted': count}), content_type='application/json')

