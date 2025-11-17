# comptes/urls.py
from django.urls import path
from .views import SignUpView

urlpatterns = [
    # Vue d'inscription
    path('signup/', SignUpView.as_view(), name='signup'),

    # Les URLS de connexion/déconnexion/réinitialisation de mot de passe
    # seront gérées par la configuration principale (voir étape 6).
]