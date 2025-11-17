# stockages/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .models import LieuStockageProfile
from .forms import LieuStockageProfileForm


# --- 1. LISTE DES LIEUX DE STOCKAGE (Read List) ---

class StockageListView(ListView):
    model = LieuStockageProfile
    template_name = 'stockages/stockage_list.html'
    context_object_name = 'stockages'
    paginate_by = 10

    def get_queryset(self):
        return LieuStockageProfile.objects.all().order_by('-date_creation')


# --- 2. DÉTAIL D'UN LIEU DE STOCKAGE (Read Detail) ---

class StockageDetailView(DetailView):
    model = LieuStockageProfile
    template_name = 'stockages/stockage_detail.html'
    context_object_name = 'profile'


# --- 3. CRÉATION DU PROFIL (Create) ---

class StockageCreateView(LoginRequiredMixin, CreateView):
    model = LieuStockageProfile
    form_class = LieuStockageProfileForm
    template_name = 'stockages/stockage_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Créer'
        return context

    def form_valid(self, form):
        # Vérifie si l'utilisateur a déjà un profil
        if LieuStockageProfile.objects.filter(user=self.request.user).exists():
            messages.error(self.request, "Vous avez déjà un profil de Lieu de Stockage. Veuillez l'éditer.")
            # Redirige vers la page d'édition ou le détail du profil existant
            return redirect('stockage_update', pk=self.request.user.stockage_profile.pk)

        # Assigne l'utilisateur actuel au profil
        form.instance.user = self.request.user
        messages.success(self.request, "Votre profil de Lieu de Stockage a été créé avec succès !")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stockage_detail', kwargs={'pk': self.object.pk})


# --- 4. MISE À JOUR DU PROFIL (Update) ---

class StockageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LieuStockageProfile
    form_class = LieuStockageProfileForm
    template_name = 'stockages/stockage_form.html'

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
        return reverse('stockage_detail', kwargs={'pk': self.object.pk})


# --- 5. SUPPRESSION DU PROFIL (Delete) ---

class StockageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LieuStockageProfile
    success_url = reverse_lazy('stockage_list')
    template_name = 'stockages/stockage_confirm_delete.html'
    context_object_name = 'profile'

    def test_func(self):
        # Autorisation : seul le propriétaire peut supprimer le profil
        profile = self.get_object()
        return profile.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Votre profil de Lieu de Stockage a été supprimé.")
        return super().form_valid(form)