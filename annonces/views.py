# annonces/views.py

from django.shortcuts import render
from django.http import HttpResponse # Importation ajoutée

def index(request):
    return HttpResponse("Bonjour, Fathi ! L'application annonces fonctionne localement.")