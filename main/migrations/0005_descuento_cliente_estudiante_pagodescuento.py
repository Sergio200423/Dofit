# Generated by Django 5.1.7 on 2025-04-19 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_duracion_tipomembresia_duraciondias_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id_descuento', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('monto', models.FloatField()),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='estudiante',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='PagoDescuento',
            fields=[
                ('id_pago_descuento', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_aplicacion', models.DateField(auto_now_add=True)),
                ('descuento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos_aplicados', to='main.descuento')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descuentos_aplicados', to='main.pago')),
            ],
        ),
    ]
