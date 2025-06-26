# DJANGO IMPORTS
from django.shortcuts import render

def backup(request):
    return render(request, 'main/backup.html')

