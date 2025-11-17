# comptes/views.py
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    """
    Vue pour l'inscription d'un nouvel utilisateur.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login') # Redirige vers la page de connexion après l'inscription
    template_name = 'registration/signup.html'