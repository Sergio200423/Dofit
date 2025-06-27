"""
Módulo utilitario para contar clientes y otros elementos relacionados.
"""
from clientes import repositorioCliente as rc
from clientes import repositorioMembresiaCliente as rmc
from django.utils.timezone import now

def contar_total_clientes():
    """Obtiene todos los clientes usando el repositorio y devuelve el total."""
    lista_clientes = rc.obtenerTodosLosClientes()
    return len(lista_clientes)

def contar_membresias_activas():
    """Cuenta cuántos clientes tienen membresía activa usando el repositorio."""
    clientes_activos = rc.obtenerClientesConMembresiaActiva()
    return clientes_activos.count() if hasattr(clientes_activos, 'count') else len(clientes_activos)

def contar_membresias_por_vencer(dias=7):
    """Cuenta cuántas membresías vencen en los próximos 'dias' días usando el repositorio."""
    return rmc.RepositorioMembresiaCliente.contar_membresias_por_vencer(dias)

def contar_membresias_expiradas():
    """Cuenta cuántas membresías ya expiraron usando el repositorio."""
    return rmc.RepositorioMembresiaCliente.contar_membresias_expiradas()

def contar_membresias_diarias_activas():
    """Cuenta clientes con membresía diaria activa."""
    return rc.obtenerClientesConMembresiaDiaria().filter(membresias_cliente__fecha_fin__gte=now().date()).count()

def contar_membresias_semanales_activas():
    """Cuenta clientes con membresía semanal activa."""
    return rc.obtenerClientesConMembresiaSemanal().filter(membresias_cliente__fecha_fin__gte=now().date()).count()

def contar_membresias_quincenales_activas():
    """Cuenta clientes con membresía quincenal activa."""
    return rc.obtenerClientesConMembresiaQuincenal().filter(membresias_cliente__fecha_fin__gte=now().date()).count()

def contar_membresias_mensuales_activas():
    """Cuenta clientes con membresía mensual activa."""
    return rc.obtenerClientesConMembresiaMensual().filter(membresias_cliente__fecha_fin__gte=now().date()).count()

# Aquí puedes agregar más funciones de conteo según necesidades futuras.
