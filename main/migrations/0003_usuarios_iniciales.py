from django.db import migrations
from django.contrib.auth.hashers import make_password

def crear_usuarios_iniciales(apps, schema_editor):
    Usuario = apps.get_model('main', 'Usuario')
    Rol = apps.get_model('main', 'Rol')
    # Buscar o crear roles
    rol_admin, _ = Rol.objects.get_or_create(nombre='admin', defaults={'descripcion': 'Administrador'})
    rol_empleado, _ = Rol.objects.get_or_create(nombre='empleado', defaults={'descripcion': 'Empleado'})
    # Crear usuarios
    Usuario.objects.create(
        nombre_usuario='admin',
        correo='sergiodanielxd2004@gmail.com',
        contra=make_password('admin'),
        rol=rol_admin
    )
    Usuario.objects.create(
        nombre_usuario='empleado',
        correo='sergiodanielxd2004+empleado@gmail.com',  # Correo diferente para evitar conflicto UNIQUE
        contra=make_password('empleado'),
        rol=rol_empleado
    )

def eliminar_usuarios_iniciales(apps, schema_editor):
    Usuario = apps.get_model('main', 'Usuario')
    Usuario.objects.filter(nombre_usuario__in=['admin', 'empleado']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(crear_usuarios_iniciales, eliminar_usuarios_iniciales),
    ]
