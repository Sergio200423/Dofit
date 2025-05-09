# Generated by Django 5.1.7 on 2025-04-19 18:58

from django.db import migrations

def add_estudiante_discount(apps, schema_editor):
    Descuento = apps.get_model('main', 'Descuento')
    Descuento.objects.create(
        nombre="Estudiante",
        monto=50,
        descripcion="Descuento para estudiantes con carnet válido"
    )

def remove_estudiante_discount(apps, schema_editor):
    # Código para revertir el descuento
    Descuento = apps.get_model('main', 'Descuento')
    Descuento.objects.filter(nombre="Estudiante").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_descuento_cliente_estudiante_pagodescuento'),
    ]

    operations = [
        migrations.RunPython(add_estudiante_discount, remove_estudiante_discount),
    ]
