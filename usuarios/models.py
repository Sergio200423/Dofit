from django.db import models

# Create your models here.
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