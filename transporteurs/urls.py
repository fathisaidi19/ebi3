# transporteurs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Liste de tous les transporteurs
    path('', views.TransporteurListView.as_view(), name='transporteur_list'),

    # Création du profil
    path('creer/', views.TransporteurCreateView.as_view(), name='transporteur_create'),

    # Détail d'un profil
    path('<int:pk>/', views.TransporteurDetailView.as_view(), name='transporteur_detail'),

    # Édition du profil
    path('<int:pk>/modifier/', views.TransporteurUpdateView.as_view(), name='transporteur_update'),

    # Suppression du profil
    path('<int:pk>/supprimer/', views.TransporteurDeleteView.as_view(), name='transporteur_delete'),
]