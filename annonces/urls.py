# annonces/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Route pour la racine de l'app (/annonces/)
]