from django.contrib.messages import get_messages

def limpiar_mensajes(request):
    """
    Elimina todos los mensajes pendientes en el request (consumir mensajes).
    """
    storage = get_messages(request)
    for _ in storage:
        pass
