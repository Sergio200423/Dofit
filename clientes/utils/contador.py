"""
Módulo utilitario para contar clientes y otros elementos relacionados.
"""
from clientes import repositorioCliente as rc
from clientes import repositorioMembresiaCliente as rmc
from django.utils.timezone import now

# Optimizado: usar .count() directamente

def contar_total_clientes():
    """Cuenta el total de clientes usando .count() para evitar cargar todos los objetos."""
    return rc.obtenerTodosLosClientes().count()

def contar_membresias_activas():
    """Cuenta cuántos clientes tienen membresía activa usando .count()."""
    return rc.obtenerClientesConMembresiaActiva().count()

def contar_membresias_por_vencer(dias=7):
    """Cuenta cuántas membresías vencen en los próximos 'dias' días usando el repositorio."""
    return rmc.RepositorioMembresiaCliente.contar_membresias_por_vencer(dias)

def contar_membresias_expiradas():
    """Cuenta cuántas membresías ya expiraron usando el repositorio."""
    return rmc.RepositorioMembresiaCliente.contar_membresias_expiradas()

def contar_membresias_diarias_activas():
    """Cuenta clientes con membresía diaria activa usando .count()."""
    return rc.obtenerClientesConMembresiaDiaria().filter(membresias_cliente__fecha_fin__gte=now().date()).count()

def contar_membresias_semanales_activas():
    """Cuenta clientes con membresía semanal activa usando .count()."""
    return rc.obtenerClientesConMembresiaSemanal().filter(membresias_cliente__fecha_fin__gte=now().date()).count()

def contar_membresias_quincenales_activas():
    """Cuenta clientes con membresía quincenal activa usando .count()."""
    return rc.obtenerClientesConMembresiaQuincenal().filter(membresias_cliente__fecha_fin__gte=now().date()).count()

def contar_membresias_mensuales_activas():
    """Cuenta clientes con membresía mensual activa usando .count()."""
    return rc.obtenerClientesConMembresiaMensual().filter(membresias_cliente__fecha_fin__gte=now().date()).count()

# Aquí puedes agregar más funciones de conteo según necesidades futuras.
