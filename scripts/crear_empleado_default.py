# Script para crear un empleado por defecto si no existe
from main.models import Empleado
from datetime import date

def crear_empleado_default():
    """Crea un empleado por defecto para el sistema si no existe"""
    try:
        # Verificar si ya existe un empleado
        empleado_default = Empleado.objects.filter(id_empleado=1).first()
        
        if not empleado_default:
            # Crear empleado por defecto
            empleado_default = Empleado.objects.create(
                id_empleado=1,
                nombre_empleado='SISTEMA',
                apellido_empleado='ADMIN',
                telefono_empleado='0000-0000',
                email_empleado='admin@sistema.local',
                direccion_empleado='N/A',
                fecha_nacimiento=date(1990, 1, 1),
                fecha_contratacion=date.today(),
                salario=0.00,
                sexo='O'
            )
            print(f"Empleado por defecto creado: {empleado_default.nombre_empleado}")
        else:
            print("Empleado por defecto ya existe")
            
        return empleado_default
        
    except Exception as e:
        print(f"Error creando empleado por defecto: {e}")
        return None

# Ejecutar la función
if __name__ == "__main__":
    crear_empleado_default()
