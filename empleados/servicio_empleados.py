# empleados/servicio_empleados.py
import re
from empleados.repositorio_empleados import RepositorioEmpleados

class ServicioEmpleados:
    """
    Servicio para operaciones de negocio relacionadas con empleados.
    """
    def __init__(self):
        self.repositorio = RepositorioEmpleados()

    def crear_empleado(self, nombre_empleado, turno, salario, **kwargs):
        # Validar que los campos no estén vacíos
        if not nombre_empleado or not turno or salario is None:
            raise ValueError("Todos los campos son obligatorios.")
        # Validar que el salario sea un número y no menor que cero
        try:
            salario = float(salario)
        except (ValueError, TypeError):
            raise ValueError("El salario debe ser un número válido.")
        if salario < 0:
            raise ValueError("El salario no puede ser menor que cero.")
        # Validar que el nombre solo contenga letras y espacios
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre_empleado):
            raise ValueError("El nombre solo puede contener letras y espacios.")
        # Validar que el turno no esté vacío
        if not turno.strip():
            raise ValueError("El turno es obligatorio.")
        # Si pasa todas las validaciones, crear el empleado
        return self.repositorio.crear_empleado(
            nombre_empleado=nombre_empleado.strip(),
            turno=turno.strip(),
            salario=salario,
            **kwargs
        )

    def obtener_empleado(self, empleado_id):
        return self.repositorio.obtener_empleado(empleado_id)

    def actualizar_empleado(self, empleado_id, **kwargs):
        return self.repositorio.actualizar_empleado(empleado_id, **kwargs)

    def eliminar_empleado(self, empleado_id):
        return self.repositorio.eliminar_empleado(empleado_id)

    def listar_empleados(self):
        return self.repositorio.listar_empleados()
