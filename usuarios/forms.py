from django import forms
from .models import Rol, Permiso, Usuario, Empleado, Administrador

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['nombre', 'descripcion']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'correo', 'contra', 'rol']
        widgets = {
            'contra': forms.PasswordInput(),
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['usuario', 'nombre_empleado', 'turno', 'salario']

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['usuario', 'nombre_administrador']
