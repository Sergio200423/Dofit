from django.db import migrations

def agregar_tipos_membresia(apps, schema_editor):
    TipoMembresia = apps.get_model('main', 'TipoMembresia')
    tipos = [
        {'nombreMembresia': 'Mensual', 'duracionDias': 30, 'precio': 500},
        {'nombreMembresia': 'Quincenal', 'duracionDias': 15, 'precio': 350},
        {'nombreMembresia': 'Semanal', 'duracionDias': 7, 'precio': 200},
        {'nombreMembresia': 'Diaria', 'duracionDias': 1, 'precio': 40},
    ]
    for tipo in tipos:
        TipoMembresia.objects.get_or_create(nombreMembresia=tipo['nombreMembresia'], defaults=tipo)

def eliminar_tipos_membresia(apps, schema_editor):
    TipoMembresia = apps.get_model('main', 'TipoMembresia')
    nombres = ['Mensual', 'Quincenal', 'Semanal', 'Diaria']
    TipoMembresia.objects.filter(nombreMembresia__in=nombres).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_usuarios_iniciales'),
    ]
    operations = [
        migrations.RunPython(agregar_tipos_membresia, eliminar_tipos_membresia),
    ]
