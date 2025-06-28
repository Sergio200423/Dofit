# servicio_usuarios.py
"""
Servicio para la lógica de negocio y validaciones del modelo Usuario.
"""
from .repositorio_usuario import RepositorioUsuario
from .servicio_roles import ServicioRoles

class ServicioUsuarios:
    @staticmethod
    def listar_usuarios():
        return RepositorioUsuario.obtener_todos()

    @staticmethod
    def obtener_usuario(usuario_id):
        return RepositorioUsuario.obtener_por_id(usuario_id)

    @staticmethod
    def crear_usuario(datos):
        # Convertir el nombre del rol a instancia de Rol
        rol_nombre = datos.get('rol')
        if rol_nombre:
            rol_obj = ServicioRoles.obtener_rol_por_nombre(rol_nombre)
            if not rol_obj:
                return None  # O lanzar excepción/retornar error
            datos['rol'] = rol_obj
        # Renombrar campo password a contra si es necesario
        if 'password' in datos:
            datos['contra'] = datos.pop('password')
        return RepositorioUsuario.crear(datos)

    @staticmethod
    def actualizar_usuario(usuario_id, datos):
        usuario = RepositorioUsuario.obtener_por_id(usuario_id)
        if usuario:
            return RepositorioUsuario.actualizar(usuario, datos)
        return None

    @staticmethod
    def eliminar_usuario(usuario_id):
        usuario = RepositorioUsuario.obtener_por_id(usuario_id)
        if usuario:
            RepositorioUsuario.eliminar(usuario)
            return True
        return False
