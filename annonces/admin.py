# annonces/admin.py
from django.contrib import admin
from .models import Annonce, Categorie, PhotoAnnonce


# Inline pour les photos
class PhotoAnnonceInline(admin.TabularInline):
    model = PhotoAnnonce
    extra = 1  # Nombre de formulaires vides à afficher
    fields = ('image', 'description', 'is_main')


# Inline pour les Sous-Annonces (enfants)
class SousAnnonceInline(admin.TabularInline):
    model = Annonce
    fk_name = 'parent_annonce'  # Clé étrangère dans le modèle Annonce
    extra = 0  # Ne pas afficher de formulaire vide par défaut
    fields = ('titre', 'prix', 'is_active', 'date_creation')
    readonly_fields = ('date_creation',)
    verbose_name = "Sous-Annonce Liée"
    verbose_name_plural = "Sous-Annonces Liées"


# Admin pour Categorie
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug',)
    prepopulated_fields = {'slug': ('nom',)}  # Génère le slug automatiquement
    search_fields = ('nom',)


# Admin pour Annonce (MODIFIÉ)
@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'depositaire', 'prix', 'date_creation', 'is_active',
                    'parent_annonce')  # Affichage du parent
    list_filter = ('is_active', 'etat', 'categorie', 'methode_livraison')
    search_fields = ('titre', 'description', 'depositaire__username')

    # Ajout des deux inlines
    inlines = [PhotoAnnonceInline, SousAnnonceInline]

    fieldsets = (
        ('Relation', {  # Nouveau Fieldset pour gérer la relation parent
            'fields': ('parent_annonce',),
            'description': "Laissez vide si c'est une annonce principale."
        }),
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