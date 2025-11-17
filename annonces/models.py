# annonces/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Assumant que ces modèles existent
from transporteurs.models import TransporteurProfile
from stockages.models import LieuStockageProfile

User = get_user_model()


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class Annonce(models.Model):
    # Choix pour l'état du produit
    ETAT_NEUF = 'NEUF'
    ETAT_OCCASION = 'OCCASION'
    ETAT_ABIME = 'ABIME'
    ETAT_CHOICES = [
        (ETAT_NEUF, 'Neuf'),
        (ETAT_OCCASION, 'Occasion'),
        (ETAT_ABIME, 'Abimé / Endommagé'),
    ]

    # Choix pour la méthode de livraison
    LIVRAISON_DEPOS = '1'
    LIVRAISON_TRANSPORT = '2'
    LIVRAISON_STOCKAGE_TRANSPORT = '3'
    LIVRAISON_CHOICES = [
        (LIVRAISON_DEPOS, '1. Dépositaire s\'occupe du transport'),
        (LIVRAISON_TRANSPORT, '2. Transporteur sélectionné'),
        (LIVRAISON_STOCKAGE_TRANSPORT, '3. Stockage + Transporteur sélectionné'),
    ]

    # Informations de base
    titre = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, related_name='annonces', on_delete=models.SET_NULL, null=True)
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES, default=ETAT_OCCASION)

    # Géolocalisation
    pays_depart = models.CharField(max_length=100)
    ville_depart = models.CharField(max_length=100)
    pays_arrivee = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    date_livraison_estimee = models.DateField(null=True, blank=True)

    # Logistique
    methode_livraison = models.CharField(max_length=1, choices=LIVRAISON_CHOICES, default=LIVRAISON_DEPOS)
    transporteur_choisi = models.ForeignKey(TransporteurProfile, related_name='annonces_assignees',
                                            on_delete=models.SET_NULL, null=True, blank=True)
    lieu_stockage_choisi = models.ForeignKey(LieuStockageProfile, related_name='annonces_stockees',
                                             on_delete=models.SET_NULL, null=True, blank=True)

    # Gestion
    depositaire = models.ForeignKey(User, related_name='mes_annonces', on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Options de paiement
    paiement_requis = models.BooleanField(default=True, verbose_name="Paiement requis à l'avance")

    class Meta:
        ordering = ('-date_creation',)
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('annonce_detail', kwargs={'pk': self.pk})

    def get_main_photo(self):
        """ Récupère la première photo (marquée comme principale ou la première téléchargée). """
        return self.photos.first()


# NOUVEAU MODÈLE POUR LES PHOTOS
class PhotoAnnonce(models.Model):
    annonce = models.ForeignKey(
        Annonce,
        related_name='photos',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='annonces_photos/',
        verbose_name="Fichier Image"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Description de l'image (Optionnel)"
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Photo principale"
    )
    date_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-is_main', 'date_upload')  # La photo principale est toujours en premier
        verbose_name = "Photo d'Annonce"
        verbose_name_plural = "Photos d'Annonce"

    def __str__(self):
        return f"Photo pour {self.annonce.titre} ({self.pk})"