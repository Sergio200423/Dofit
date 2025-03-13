from django.contrib import admin
from .models import Empleado, Membresia, Cliente, Asistencia, Producto, Pago, PagoProducto

admin.site.register(Empleado)
admin.site.register(Membresia)
admin.site.register(Cliente)
admin.site.register(Asistencia)
admin.site.register(Producto)
admin.site.register(Pago)
admin.site.register(PagoProducto)
