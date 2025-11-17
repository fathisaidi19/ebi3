# messagerie/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Boîte de réception (Liste des conversations)
    path('', views.ConversationListView.as_view(), name='conversation_list'),

    # Démarrer une nouvelle conversation
    path('demarrer/<int:user_id>/', views.start_conversation, name='start_conversation_user'),
    path('demarrer/<int:user_id>/annonce/<int:annonce_pk>/', views.start_conversation,
         name='start_conversation_annonce'),

    # Afficher le détail de la conversation et envoyer un message
    path('<int:pk>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
]