# transporteurs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .models import TransporteurProfile
from .forms import TransporteurProfileForm


# --- 1. LISTE DES TRANSPORTEURS (Read List) ---

class TransporteurListView(ListView):
    model = TransporteurProfile
    template_name = 'transporteurs/transporteur_list.html'
    context_object_name = 'transporteurs'
    paginate_by = 10

    def get_queryset(self):
        return TransporteurProfile.objects.all().order_by('-date_creation')


# --- 2. DÉTAIL D'UN TRANSPORTEUR (Read Detail) ---

class TransporteurDetailView(DetailView):
    model = TransporteurProfile
    template_name = 'transporteurs/transporteur_detail.html'
    context_object_name = 'profile'


# --- 3. CRÉATION DU PROFIL (Create) ---

class TransporteurCreateView(LoginRequiredMixin, CreateView):
    model = TransporteurProfile
    form_class = TransporteurProfileForm
    template_name = 'transporteurs/transporteur_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Créer'
        return context

    def form_valid(self, form):
        # Vérifie si l'utilisateur a déjà un profil
        if TransporteurProfile.objects.filter(user=self.request.user).exists():
            messages.error(self.request, "Vous avez déjà un profil Transporteur. Veuillez l'éditer.")
            # Redirige vers la page d'édition ou le détail du profil existant
            return redirect('transporteur_update', pk=self.request.user.transporteur_profile.pk)

        # Assigne l'utilisateur actuel au profil
        form.instance.user = self.request.user
        messages.success(self.request, "Votre profil Transporteur a été créé avec succès !")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('transporteur_detail', kwargs={'pk': self.object.pk})


# --- 4. MISE À JOUR DU PROFIL (Update) ---

class TransporteurUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TransporteurProfile
    form_class = TransporteurProfileForm
    template_name = 'transporteurs/transporteur_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Modifier'
        return context

    def test_func(self):
        # Autorisation : seul le propriétaire du profil peut le modifier
        profile = self.get_object()
        return profile.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Votre profil a été mis à jour avec succès.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('transporteur_detail', kwargs={'pk': self.object.pk})


# --- 5. SUPPRESSION DU PROFIL (Delete) ---

class TransporteurDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TransporteurProfile
    success_url = reverse_lazy('transporteur_list')
    template_name = 'transporteurs/transporteur_confirm_delete.html'
    context_object_name = 'profile'

    def test_func(self):
        # Autorisation : seul le propriétaire peut supprimer le profil
        profile = self.get_object()
        return profile.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Votre profil Transporteur a été supprimé.")
        return super().form_valid(form)