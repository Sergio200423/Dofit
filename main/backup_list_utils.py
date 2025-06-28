import os
from django.conf import settings
from datetime import datetime

def list_backups():
    """
    Devuelve una lista de backups en la carpeta 'backups', ordenados por fecha de creación descendente,
    incluyendo nombre y tamaño en bytes.
    """
    backups_dir = os.path.join(settings.BASE_DIR, 'backups')
    if not os.path.exists(backups_dir):
        return {'backups': [], 'total_size': 0}
    backups = []
    total_size = 0
    for f in os.listdir(backups_dir):
        if f.startswith('backup_dofit_') and f.endswith('.json'):
            path = os.path.join(backups_dir, f)
            size = os.path.getsize(path)
            total_size += size
            backups.append({'name': f, 'size': size})
    backups.sort(key=lambda x: x['name'], reverse=True)
    return {'backups': backups, 'total_size': total_size}
