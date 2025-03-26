from django.db import models
from datetime import timedelta, date

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre_empleado = models.CharField(max_length=50, null=True, blank=True)
    turno = models.CharField(max_length=10, null=True, blank=True)
    salario = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre_empleado


class Membresia(models.Model):
    id_membresia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=True, blank=True)
    duracion = models.IntegerField(null=True, blank=True)  # Duración en días
    precio = models.FloatField(null=True, blank=True)

    @property
    def estado(self):
        if not self.fecha_inicio or not self.duracion:
            return "Sin inicio o duración"
        fecha_fin = self.fecha_inicio + timedelta(days=self.duracion)
        return 'Activa' if fecha_fin >= date.today() else 'Expirada'

    def __str__(self):
        return f"Membresía {self.id_membresia} - ${self.precio}"

class Cliente(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=50, null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=[('F', 'Femenino'), ('M', 'Masculino')], default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, related_name="clientes")
    membresia = models.ForeignKey(Membresia, on_delete=models.SET_NULL, null=True, related_name="clientes")  # Cambiado de id_membresia a membresia
    estado = models.CharField(max_length=30, choices=ESTADOS, default='Activo')
    fecha_inicio = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre_cliente

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, related_name="asistencias")
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name="asistencias")

    def __str__(self):
        return f"Asistencia {self.id_asistencia} - {self.fecha}"

class Producto(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('agotado', 'Agotado'),
    ]
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=25, null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    descripcion = models.CharField(max_length=80, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    existencia = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default='Disponible')

    def __str__(self):
        return self.nombre_producto


class Pago(models.Model):
    TIPO_CHOICES = [
        ('Membresia', 'Membresía'),
        ('Producto', 'Producto'),
    ]
    
    id_pago = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='Membresia')  # Tipo de pago
    fecha = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pagos")
    total_a_pagar = models.FloatField(null=True, blank=True)
    
    def calcular_total_a_pagar(self):
        if self.tipo == 'Producto':
            productos_pagados = self.productospagados.all()
            total = sum(pp.cantidad * pp.producto.precio for pp in productos_pagados)
            return total
        return 0

    def save(self, *args, **kwargs):
        # Calcula el total antes de guardar
        if not self.total_a_pagar:
            self.total_a_pagar = self.calcular_total_a_pagar()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pago {self.id_pago} - {self.tipo} - ${self.total_a_pagar}"



class PagoProducto(models.Model):
    id_pago_producto = models.AutoField(primary_key=True)
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name="productospagados")  # Relación con el pago
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="ventas")
    fecha_pago = models.DateField(null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)

    def total_a_pagar(self):
        return self.cantidad * self.producto.precio
        

    def __str__(self):
        return f"PagoProducto {self.id_pago_producto} - {self.cantidad} x {self.producto.nombre_producto}"