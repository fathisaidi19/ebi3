# annonces/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # La page d'accueil de l'application annonces affichera la liste des annonces
    path('', views.AnnonceListView.as_view(), name='annonce_list'),
    path('deposer/', views.AnnonceCreateView.as_view(), name='annonce_create'),
    path('<int:pk>/', views.AnnonceDetailView.as_view(), name='annonce_detail'),
]