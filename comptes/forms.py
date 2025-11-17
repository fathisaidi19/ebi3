# comptes/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

# Obtenir le modèle User actif (pour les modèles personnalisés)
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé basé sur UserCreationForm de Django.
    """

    class Meta:
        model = User
        fields = ('username', 'email')  # Champs pour l'inscription


class CustomUserChangeForm(UserChangeForm):
    """
    Formulaire pour la modification du profil utilisateur (pour l'admin).
    """

    class Meta:
        model = User
        fields = ('username', 'email')