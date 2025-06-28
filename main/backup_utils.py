import os
from datetime import datetime

def get_next_backup_filename(backup_dir):
    """
    Genera el siguiente nombre de archivo para backup en formato backup_dofit_AAAA_NNNN.json
    donde AAAA es el año actual y NNNN es un contador de 4 dígitos.
    Si no hay backups, comienza en 0001.
    """
    year = datetime.now().year
    prefix = f"backup_dofit_{year}_"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    existing = [f for f in os.listdir(backup_dir) if f.startswith(prefix) and f.endswith('.json')]
    numbers = []
    for fname in existing:
        try:
            num = int(fname.replace(prefix, '').replace('.json', ''))
            numbers.append(num)
        except ValueError:
            continue
    next_num = max(numbers) + 1 if numbers else 1
    return f"{prefix}{next_num:04d}.json"

def delete_all_backups(backup_dir):
    """
    Elimina todos los archivos de backup en el directorio backups.
    """
    if not os.path.exists(backup_dir):
        return 0
    count = 0
    for f in os.listdir(backup_dir):
        if f.startswith('backup_dofit_') and f.endswith('.json'):
            try:
                os.remove(os.path.join(backup_dir, f))
                count += 1
            except Exception:
                continue
    return count
