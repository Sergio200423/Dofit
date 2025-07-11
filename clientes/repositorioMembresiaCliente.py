from main.models import MembresiaCliente, Cliente, TipoMembresia
from django.utils.timezone import now
from django.db import IntegrityError
from datetime import timedelta

class RepositorioMembresiaCliente:
    @staticmethod
    def crear_membresia_cliente(id_cliente, id_membresia, fecha_inicio=None):
        """
        Crea una nueva MembresiaCliente. Si el cliente tiene membresías activas o futuras, la nueva se programa para iniciar después de la última.
        """
        try:
            cliente = Cliente.objects.get(id_cliente=id_cliente)
            membresia = TipoMembresia.objects.get(id_membresia=id_membresia)
            from datetime import datetime
            hoy = now().date()
            # Buscar la última membresía futura o activa (la de mayor fecha_fin >= hoy)
            ultima = cliente.membresias_cliente.filter(fecha_fin__gte=hoy).order_by('-fecha_fin').first()
            if ultima:
                fecha_inicio_real = ultima.fecha_fin
            else:
                # Si no hay membresía activa o futura, inicia hoy o la fecha indicada
                if fecha_inicio is None:
                    fecha_inicio_real = hoy
                elif isinstance(fecha_inicio, str):
                    fecha_inicio_real = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                else:
                    fecha_inicio_real = fecha_inicio
            fecha_fin = fecha_inicio_real + timedelta(days=membresia.duracionDias)
            membresia_cliente = MembresiaCliente.objects.create(
                cliente=cliente,
                membresia=membresia,
                fecha_inicio=fecha_inicio_real,
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
        Obtiene la membresía activa de un cliente (fecha_inicio <= hoy <= fecha_fin).
        """
        try:
            cliente = Cliente.objects.get(id_cliente=id_cliente)
            hoy = now().date()
            membresia_activa = cliente.membresias_cliente.filter(fecha_inicio__lte=hoy, fecha_fin__gte=hoy).order_by('fecha_inicio').first()
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
    
    @staticmethod
    def contar_membresias_por_vencer(dias=7):
        """Cuenta cuántas membresías vencen en los próximos 'dias' días."""
        hoy = now().date()
        hasta = hoy + timedelta(days=dias)
        return MembresiaCliente.objects.filter(fecha_fin__gt=hoy, fecha_fin__lte=hasta).count()
    
    @staticmethod
    def contar_membresias_expiradas():
        """Cuenta cuántas membresías ya expiraron (fecha_fin < hoy)."""
        hoy = now().date()
        return MembresiaCliente.objects.filter(fecha_fin__lt=hoy).count()
    
    @staticmethod
    def obtener_membresias_por_vencer(dias=7):
        """Devuelve una lista de MembresiaCliente que vencen en los próximos 'dias' días."""
        hoy = now().date()
        hasta = hoy + timedelta(days=dias)
        return MembresiaCliente.objects.filter(fecha_fin__gt=hoy, fecha_fin__lte=hasta)

    @staticmethod
    def obtener_membresias_expiradas():
        """Devuelve una lista de MembresiaCliente que ya expiraron (fecha_fin < hoy)."""
        hoy = now().date()
        return MembresiaCliente.objects.filter(fecha_fin__lt=hoy)