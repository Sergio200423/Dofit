# Script para verificar la estructura del modelo Cliente
from main.models import Cliente

def verificar_campos_cliente():
    """Verifica los campos disponibles en el modelo Cliente"""
    try:
        # Obtener todos los campos del modelo Cliente
        campos = [field.name for field in Cliente._meta.get_fields()]
        
        print("Campos disponibles en el modelo Cliente:")
        for campo in sorted(campos):
            print(f"  - {campo}")
            
        # Verificar si existe algún cliente
        total_clientes = Cliente.objects.count()
        print(f"\nTotal de clientes en la base de datos: {total_clientes}")
        
        if total_clientes > 0:
            # Mostrar un ejemplo de cliente
            cliente_ejemplo = Cliente.objects.first()
            print(f"\nEjemplo de cliente:")
            print(f"  ID: {cliente_ejemplo.id_cliente}")
            print(f"  Nombre: {getattr(cliente_ejemplo, 'nombre_cliente', 'N/A')}")
            print(f"  Empleado ID: {getattr(cliente_ejemplo, 'empleado_id', 'N/A')}")
            
    except Exception as e:
        print(f"Error verificando modelo Cliente: {e}")

# Ejecutar la función
if __name__ == "__main__":
    verificar_campos_cliente()
