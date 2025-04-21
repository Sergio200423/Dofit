from django.contrib import admin
from .models import Empleado, TipoMembresia, Cliente, Asistencia, Producto, Pago, PagoProducto, MembresiaCliente

admin.site.register(Empleado)
admin.site.register(TipoMembresia)
admin.site.register(Cliente)
admin.site.register(Asistencia)
admin.site.register(Producto)
admin.site.register(Pago)
admin.site.register(PagoProducto)
admin.site.register(MembresiaCliente)
