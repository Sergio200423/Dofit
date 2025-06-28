from usuarios.models import Empleado
from django.core.exceptions import ObjectDoesNotExist

class RepositorioEmpleados:
    @staticmethod
    def crear_empleado(**kwargs):
        return Empleado.objects.create(**kwargs)

    @staticmethod
    def obtener_empleado_por_id(empleado_id):
        try:
            return Empleado.objects.get(id=empleado_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def listar_empleados():
        return Empleado.objects.all()

    @staticmethod
    def actualizar_empleado(empleado_id, **kwargs):
        empleado = RepositorioEmpleados.obtener_empleado_por_id(empleado_id)
        if empleado:
            for key, value in kwargs.items():
                setattr(empleado, key, value)
            empleado.save()
            return empleado
        return None

    @staticmethod
    def eliminar_empleado(empleado_id):
        empleado = RepositorioEmpleados.obtener_empleado_por_id(empleado_id)
        if empleado:
            empleado.delete()
            return True
        return False
