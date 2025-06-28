# servicio_roles.py
"""
Servicio para la lógica de negocio y validaciones del modelo Rol.
"""
from .repositorio_roles import RepositorioRoles

class ServicioRoles:
    @staticmethod
    def listar_roles():
        return RepositorioRoles.obtener_todos()

    @staticmethod
    def obtener_rol(rol_id):
        return RepositorioRoles.obtener_por_id(rol_id)

    @staticmethod
    def crear_rol(datos):
        # Aquí puedes agregar validaciones antes de crear
        return RepositorioRoles.crear(datos)

    @staticmethod
    def actualizar_rol(rol_id, datos):
        rol = RepositorioRoles.obtener_por_id(rol_id)
        if rol:
            return RepositorioRoles.actualizar(rol, datos)
        return None

    @staticmethod
    def eliminar_rol(rol_id):
        rol = RepositorioRoles.obtener_por_id(rol_id)
        if rol:
            RepositorioRoles.eliminar(rol)
            return True
        return False

    @staticmethod
    def obtener_rol_por_nombre(nombre):
        return RepositorioRoles.obtener_por_nombre(nombre)
