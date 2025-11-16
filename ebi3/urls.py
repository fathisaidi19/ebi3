# ebi3/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse # <-- AJOUTEZ CETTE LIGNE

def welcome_view(request): # <-- AJOUTEZ CETTE FONCTION
    return HttpResponse("Bienvenue sur le projet ebi3 ! Base en cours de construction.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('annonces/', include('annonces.urls')),
    path('', welcome_view, name='home'), # <-- AJOUTEZ CETTE LIGNE
]