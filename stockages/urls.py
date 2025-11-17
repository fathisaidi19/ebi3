# stockages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Liste de tous les lieux de stockage
    path('', views.StockageListView.as_view(), name='stockage_list'),

    # Création du profil
    path('creer/', views.StockageCreateView.as_view(), name='stockage_create'),

    # Détail d'un profil
    path('<int:pk>/', views.StockageDetailView.as_view(), name='stockage_detail'),

    # Édition du profil
    path('<int:pk>/modifier/', views.StockageUpdateView.as_view(), name='stockage_update'),

    # Suppression du profil
    path('<int:pk>/supprimer/', views.StockageDeleteView.as_view(), name='stockage_delete'),
]