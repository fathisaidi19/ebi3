# annonces/admin.py
from django.contrib import admin
from .models import Annonce, Categorie, PhotoAnnonce  # Importation de PhotoAnnonce


# Inline pour les photos
class PhotoAnnonceInline(admin.TabularInline):
    model = PhotoAnnonce
    extra = 1  # Nombre de formulaires vides à afficher
    fields = ('image', 'description', 'is_main')


# Admin pour Categorie (Correction : retrait des références à 'parent')
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug',)
    prepopulated_fields = {'slug': ('nom',)}  # Génère le slug automatiquement
    search_fields = ('nom',)


# Admin pour Annonce
@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'depositaire', 'prix', 'date_creation', 'is_active')
    list_filter = ('is_active', 'etat', 'categorie', 'methode_livraison')
    search_fields = ('titre', 'description', 'depositaire__username')
    inlines = [PhotoAnnonceInline]  # Ajout de l'inline pour les photos

    fieldsets = (
        ('Informations Générales', {
            'fields': ('depositaire', 'titre', 'description', 'prix', 'categorie', 'etat')
        }),
        ('Itinéraire et Logistique', {
            'fields': ('pays_depart', 'ville_depart', 'pays_arrivee', 'ville_arrivee', 'date_livraison_estimee',
                       'methode_livraison', 'transporteur_choisi', 'lieu_stockage_choisi')
        }),
        ('Statut', {
            'fields': ('paiement_requis', 'is_active'),
        }),
    )


# Admin pour PhotoAnnonce (pour gestion directe si nécessaire)
@admin.register(PhotoAnnonce)
class PhotoAnnonceAdmin(admin.ModelAdmin):
    list_display = ('image', 'annonce', 'is_main', 'date_upload')
    list_filter = ('is_main',)
    search_fields = ('annonce__titre', 'description')