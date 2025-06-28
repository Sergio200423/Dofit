# repositorio_roles.py
"""
Repositorio para operaciones de acceso a datos del modelo Rol.
"""
from .models import Rol

class RepositorioRoles:
    @staticmethod
    def obtener_todos():
        return Rol.objects.all()

    @staticmethod
    def obtener_por_id(rol_id):
        return Rol.objects.filter(id=rol_id).first()

    @staticmethod
    def crear(datos):
        return Rol.objects.create(**datos)

    @staticmethod
    def actualizar(rol, datos):
        for key, value in datos.items():
            setattr(rol, key, value)
        rol.save()
        return rol

    @staticmethod
    def eliminar(rol):
        rol.delete()

    @staticmethod
    def obtener_por_nombre(nombre):
        return Rol.objects.filter(nombre__iexact=nombre).first()
