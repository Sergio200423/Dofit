import random
from django.shortcuts import render

def generar_codigo_verificacion():
    # Genera un número aleatorio de 4 dígitos
    return random.randint(1000, 9999)

