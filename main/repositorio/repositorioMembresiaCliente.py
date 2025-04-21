from main.models import MembresiaCliente, Cliente, TipoMembresia
from django.utils.timezone import now
from django.db import IntegrityError
from datetime import timedelta

class RepositorioMembresiaCliente:
    @staticmethod
    def crear_membresia_cliente(id_cliente, id_membresia, fecha_inicio):
        """
        Crea una nueva MembresiaCliente.
        """
        try:
            cliente = Cliente.objects.get(id_cliente=id_cliente)
            membresia = TipoMembresia.objects.get(id_membresia=id_membresia)
            # Asegurarse de que fecha_inicio sea un objeto de tipo datetime.date
            if isinstance(fecha_inicio, str):
                from datetime import datetime
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

        # Calcular fecha_fin
            fecha_fin = fecha_inicio + timedelta(days=membresia.duracionDias)

            membresia_cliente = MembresiaCliente.objects.create(
                cliente=cliente,
                membresia=membresia,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            return {"success": True, "membresia_cliente": membresia_cliente}
        except Cliente.DoesNotExist:
            return {"success": False, "error": "Cliente no encontrado."}
        except TipoMembresia.DoesNotExist:
            return {"success": False, "error": "Tipo de membresía no encontrado."}
        except IntegrityError as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def obtener_membresias_cliente(id_cliente):
        """
        Obtiene todas las membresías asociadas a un cliente.
        """
        try:
            cliente = Cliente.objects.get(id_cliente=id_cliente)
            membresias = cliente.membresias_cliente.all()
            return {"success": True, "membresias": membresias}
        except Cliente.DoesNotExist:
            return {"success": False, "error": "Cliente no encontrado."}
        
    @staticmethod
    def obtener_membresia_activa(id_cliente):
        """
        Obtiene la membresía activa de un cliente (aquella cuya fecha de fin no ha caducado).
        :param id_cliente: ID del cliente
        :return: Diccionario con la membresía activa o un mensaje de error
        """
        try:
            cliente = Cliente.objects.get(id_cliente=id_cliente)
            membresia_activa = cliente.membresias_cliente.filter(fecha_fin__gte=now().date()).first()
            if membresia_activa:
                return {"success": True, "membresia_activa": membresia_activa}
            return {"success": False, "error": "El cliente no tiene una membresía activa."}
        except Cliente.DoesNotExist:
            return {"success": False, "error": "Cliente no encontrado."}

    @staticmethod
    def actualizar_membresia_cliente(id_membresia_cliente, id_membresia):
        """
        Actualiza la membresía de un cliente.
        """
        try:
            membresia_cliente = MembresiaCliente.objects.get(id_membresia_cliente=id_membresia_cliente)
            nueva_membresia = TipoMembresia.objects.get(id_membresia=id_membresia)
            fecha_inicio = now().date()
            fecha_fin = fecha_inicio + timedelta(days=nueva_membresia.duracionDias)

            membresia_cliente.membresia = nueva_membresia
            membresia_cliente.fecha_inicio = fecha_inicio
            membresia_cliente.fecha_fin = fecha_fin
            membresia_cliente.save()

            return {"success": True, "membresia_cliente": membresia_cliente}
        except MembresiaCliente.DoesNotExist:
            return {"success": False, "error": "Membresía del cliente no encontrada."}
        except TipoMembresia.DoesNotExist:
            return {"success": False, "error": "Tipo de membresía no encontrado."}
        except IntegrityError as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def eliminar_membresia_cliente(id_membresia_cliente):
        """
        Elimina una membresía de cliente.
        """
        try:
            membresia_cliente = MembresiaCliente.objects.get(id_membresia_cliente=id_membresia_cliente)
            membresia_cliente.delete()
            return {"success": True, "message": "Membresía del cliente eliminada correctamente."}
        except MembresiaCliente.DoesNotExist:
            return {"success": False, "error": "Membresía del cliente no encontrada."}