# repositorio_usuario.py
"""
Repositorio para operaciones de acceso a datos del modelo Usuario.
"""
from .models import Usuario

class RepositorioUsuario:
    @staticmethod
    def obtener_todos():
        return Usuario.objects.all()

    @staticmethod
    def obtener_por_id(usuario_id):
        return Usuario.objects.filter(id_usuario=usuario_id).first()

    @staticmethod
    def crear(datos):
        return Usuario.objects.create(**datos)

    @staticmethod
    def actualizar(usuario, datos):
        for key, value in datos.items():
            setattr(usuario, key, value)
        usuario.save()
        return usuario

    @staticmethod
    def eliminar(usuario):
        usuario.delete()
