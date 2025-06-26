from django.db import models
from datetime import timedelta, date
from django.utils import timezone

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    # Relación con Permiso ahora será a través de RolPermiso

    def __str__(self):
        return self.nombre

class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='rol_permisos')
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE, related_name='permiso_roles')

    class Meta:
        unique_together = ('rol', 'permiso')
        verbose_name = 'Rol-Permiso'
        verbose_name_plural = 'Roles-Permisos'

    def __str__(self):
        return f"{self.rol.nombre} - {self.permiso.nombre}"

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(max_length=100, unique=True, null=True, blank=True)  # Nuevo campo correo electrónico
    contra = models.CharField(max_length=128)  # Hasheada
    n_intentos = models.IntegerField(default=0) #Intentos de inicio de sesion
    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, related_name='usuarios')

    def __str__(self):
        return self.nombre_usuario

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='empleado', null=True, blank=True, unique=True)
    nombre_empleado = models.CharField(max_length=50, null=True, blank=True)
    turno = models.CharField(max_length=10, null=True, blank=True)
    salario = models.FloatField(null=True, blank=True)
    # Nota: Controla en la lógica de negocio que cada usuario tenga solo un perfil (Empleado o Administrador)
    def __str__(self):
        return self.nombre_empleado

class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='administrador', null=True, blank=True, unique=True)
    nombre_administrador = models.CharField(max_length=50, null=True, blank=True)
    # Nota: Controla en la lógica de negocio que cada usuario tenga solo un perfil (Empleado o Administrador)
    def __str__(self):
        return self.nombre_administrador or self.usuario.nombre_usuario
    
class TipoMembresia(models.Model):
    id_membresia = models.AutoField(primary_key=True)
    nombreMembresia = models.CharField(max_length=30, null=True, blank=True)
    duracionDias = models.IntegerField(null=True, blank=True)  # Duración en días
    precio = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Membresía {self.nombreMembresia} - C${self.precio}"


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=50, null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=[('F', 'Femenino'), ('M', 'Masculino')], default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, related_name="clientes")
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)
    estudiante = models.CharField(max_length=20, null=True, blank=True)  # Número de carnet del estudiante

    def __str__(self):
        return self.nombre_cliente


class MembresiaCliente(models.Model):
    id_membresia_cliente = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="membresias_cliente")
    membresia = models.ForeignKey(TipoMembresia, on_delete=models.CASCADE, related_name="membresias_cliente")
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    @property
    def estado(self):
        """
        Calcula si la membresía está activa o inactiva.
        """
        if self.fecha_fin and self.fecha_inicio:
            return 'activo' if self.fecha_fin > timezone.now().date() else 'inactivo'
        return 'inactivo'

    def __str__(self):
        return f"MembresíaCliente {self.id_membresia_cliente} - {self.cliente.nombre_cliente} - {self.estado}"


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

    TIPOS = [
        ('Barra energetica', 'Barra energética'),
        ('Proteina', 'Proteína'),
        ('Vitaminas', 'Vitaminas'),
        ('Suplementos', 'Suplementos'),
        ('Bebidas', 'Bebidas'),
        ('Caramelos', 'Caramelos'),
    ]

    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=25, null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    descripcion = models.CharField(max_length=80, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    existencia = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default="suplementos")
    estado = models.CharField(max_length=30, choices=ESTADOS, default='Disponible')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre_producto


class Descuento(models.Model):
    id_descuento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, blank=False)  # Nombre del descuento (e.g., "Estudiante")
    monto = models.FloatField(null=False, blank=False)  # Monto del descuento (e.g., 50 pesos)
    descripcion = models.TextField(null=True, blank=True)  # Descripción opcional del descuento

    def __str__(self):
        return f"{self.nombre} - C${self.monto}"
    
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

    def save(self, *args, **kwargs):
        # Guardar el pago sin calcular descuentos
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pago {self.id_pago} - {self.tipo} - C${self.total_a_pagar}"

class PagoDescuento(models.Model):
    id_pago_descuento = models.AutoField(primary_key=True)
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name="descuentos_aplicados")  # Relación con Pago
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE, related_name="pagos_aplicados")  # Relación con Descuento
    fecha_aplicacion = models.DateField(auto_now_add=True)  # Fecha en que se aplicó el descuento

    def aplicar_descuento(self):
        """
        Aplica el descuento al total del pago.
        """
        print("Iniciando la función aplicar_descuento...")
        print(f"Pago antes del descuento: {self.pago.total_a_pagar}")
        print(f"Descuento a aplicar: {self.descuento.monto}")

        if self.pago and self.descuento:
            # Inicializar total_a_pagar si es None
            if self.pago.total_a_pagar is None:
                self.pago.total_a_pagar = 0
                print("El total_a_pagar era None. Inicializado a 0.")

            # Aplicar el descuento
            self.pago.total_a_pagar = max(self.pago.total_a_pagar - self.descuento.monto, 0)  # Asegúrate de que no sea negativo
            print(f"Pago después del descuento: {self.pago.total_a_pagar}")

            # Guardar los cambios en el pago
            self.pago.save()
            print("Descuento aplicado y pago actualizado en la base de datos.")
        else:
            print("Error: El pago o el descuento no son válidos.")

    def save(self, *args, **kwargs):
        # Aplicar el descuento automáticamente al guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pago {self.pago.id_pago} - Descuento {self.descuento.nombre} (${self.descuento.monto})"
    
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

class Maquina(models.Model):
    ESTADOS = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ]
    
    RAZON_INACTIVIDAD = [
        ('reparacion', 'En Reparación'),
        ('mal_estado', 'Mal Estado'),
        ('mantenimiento', 'Mantenimiento Preventivo'),
        ('otra', 'Otra Razón'),
        ('no_aplica', 'No Aplica'),
    ]

    id_maquina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activa')
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='maquinas/', null=True, blank=True)
    
    # Nuevos campos para máquinas inactivas
    razon_inactividad = models.CharField(max_length=20, choices=RAZON_INACTIVIDAD, default='no_aplica')
    fecha_inactividad = models.DateField(null=True, blank=True)
    notas_inactividad = models.TextField(null=True, blank=True)
    fecha_estimada_reparacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.estado}"

