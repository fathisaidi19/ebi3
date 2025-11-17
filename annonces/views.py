# annonces/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect  # Importation nécessaire

from .models import Annonce, Categorie, PhotoAnnonce  # PhotoAnnonce ajouté
from .forms import AnnonceForm, PhotoAnnonceFormSet  # PhotoAnnonceFormSet ajouté


# Les importations de transporteurs/stockages sont implicites ou via Annonce

# --- VUE 1 : LISTE ET RECHERCHE ---
class AnnonceListView(ListView):
    model = Annonce
    template_name = 'annonces/annonce_list.html'
    context_object_name = 'annonces'
    paginate_by = 10

    def get_queryset(self):
        queryset = Annonce.objects.all().order_by('-date_creation')

        # Logique de filtrage basée sur les paramètres GET (similaire au template)
        query = self.request.GET.get('q')
        ville_depart = self.request.GET.get('ville_depart')
        ville_arrivee = self.request.GET.get('ville_arrivee')
        categorie_id = self.request.GET.get('categorie')
        etat = self.request.GET.get('etat')
        date_max = self.request.GET.get('date_livraison')
        methode_logistique = self.request.GET.get('methode_logistique')

        if query:
            queryset = queryset.filter(
                Q(titre__icontains=query) |
                Q(description__icontains=query)
            )

        if ville_depart:
            queryset = queryset.filter(ville_depart__icontains=ville_depart)
        if ville_arrivee:
            queryset = queryset.filter(ville_arrivee__icontains=ville_arrivee)

        if categorie_id:
            queryset = queryset.filter(categorie__id=categorie_id)
        if etat:
            queryset = queryset.filter(etat=etat)
        if date_max:
            queryset = queryset.filter(date_livraison_estimee__lte=date_max)
        if methode_logistique:
            queryset = queryset.filter(methode_livraison=methode_logistique)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assumant que Categorie existe pour les filtres
        context['categories'] = Categorie.objects.all()
        context['etats'] = Annonce.ETAT_CHOICES
        context['methodes_livraison'] = Annonce.LIVRAISON_CHOICES
        context['current_query'] = self.request.GET
        return context


# --- VUE 2 : DÉTAIL ---
class AnnonceDetailView(DetailView):
    model = Annonce
    template_name = 'annonces/annonce_detail.html'
    context_object_name = 'annonce'

    # (La méthode get_context_data pour les photos est assumée existante)


# --- VUE 3 : CRÉATION (MODIFIÉE pour FormSet) ---
class AnnonceCreateView(LoginRequiredMixin, CreateView):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'annonces/annonce_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # S'assurer que le formset est inclus pour l'affichage
        if self.request.POST:
            # Si POST, lier les données soumises au FormSet
            context['photo_formset'] = PhotoAnnonceFormSet(self.request.POST, self.request.FILES)
        else:
            # Sinon, afficher un FormSet vide
            context['photo_formset'] = PhotoAnnonceFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']

        # 1. Assigner l'utilisateur (depositaire)
        form.instance.depositaire = self.request.user

        # 2. Vérifier la validité du formulaire principal ET du formset
        if form.is_valid() and photo_formset.is_valid():
            self.object = form.save()

            # 3. Enregistrer les Photos en liant l'instance Annonce
            photo_formset.instance = self.object
            photo_formset.save()

            messages.success(self.request, "Votre annonce et vos photos ont été déposées avec succès.")
            return HttpResponseRedirect(self.get_success_url())
        else:
            # Si le formset ou le formulaire principal n'est pas valide
            messages.error(self.request, "Erreur dans le formulaire. Veuillez corriger les erreurs.")
            # Passer par form_invalid pour réafficher le formulaire avec les erreurs
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Surcharge pour s'assurer que le formset (avec ses erreurs) est bien présent
        context = self.get_context_data()
        context['form'] = form  # Passer le formulaire principal avec erreurs
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('annonce_detail', kwargs={'pk': self.object.pk})


# --- VUE 4 : MISE À JOUR (MODIFIÉE pour FormSet) ---
class AnnonceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'annonces/annonce_form.html'

    def test_func(self):
        # Autorisation : seul le dépositaire peut modifier
        annonce = self.get_object()
        return annonce.depositaire == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialiser le formset avec l'instance existante
        if self.request.POST:
            # Si POST, lier les données soumises et les fichiers à l'instance
            context['photo_formset'] = PhotoAnnonceFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            # Sinon, charger les données existantes pour l'instance
            context['photo_formset'] = PhotoAnnonceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']

        # 1. Enregistrer l'Annonce (form.save())
        self.object = form.save()

        # 2. Valider et enregistrer les Photos (y compris la suppression)
        if photo_formset.is_valid():
            photo_formset.instance = self.object
            photo_formset.save()
            messages.success(self.request, "Votre annonce et vos photos ont été mises à jour avec succès.")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, "Erreur dans le formulaire de photo. Veuillez corriger les erreurs.")
            # Revenir pour afficher les erreurs
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Surcharge pour s'assurer que le formset (avec ses erreurs) est bien présent
        context = self.get_context_data()
        context['form'] = form  # Passer le formulaire principal avec erreurs
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('annonce_detail', kwargs={'pk': self.object.pk})


# --- VUE 5 : SUPPRESSION ---
class AnnonceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Annonce
    success_url = reverse_lazy('annonce_list')
    template_name = 'annonces/annonce_confirm_delete.html'
    context_object_name = 'annonce'

    def test_func(self):
        annonce = self.get_object()
        return annonce.depositaire == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Votre annonce a été supprimée.")
        return super().form_valid(form)