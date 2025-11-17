# stockages/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class LieuStockageProfile(models.Model):
    """
    Modèle représentant le profil détaillé d'un lieu ou d'un service de stockage.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='stockage_profile',
        verbose_name="Utilisateur lié"
    )
    nom_lieu = models.CharField(max_length=150, unique=True, verbose_name="Nom du Lieu de Stockage")
    description = models.TextField(verbose_name="Description des services de stockage",
                                   help_text="Décrivez l'espace, la sécurité, et les conditions de stockage.")

    # Capacité et Conditions
    superficie_m2 = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Superficie (m²)")
    temperature_controle = models.BooleanField(default=False, verbose_name="Température contrôlée")
    securite_24_7 = models.BooleanField(default=False, verbose_name="Sécurité 24/7 (Alarme/Vidéo)")

    # Coordonnées / Localisation
    pays = models.CharField(max_length=50, verbose_name="Pays")
    ville = models.CharField(max_length=50, verbose_name="Ville")
    adresse_complete = models.CharField(max_length=255, verbose_name="Adresse (Visible seulement après accord)")

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil Lieu de Stockage"
        verbose_name_plural = "Profils Lieux de Stockage"

    def __str__(self):
        return self.nom_lieu

    def get_absolute_url(self):
        return reverse('stockage_detail', kwargs={'pk': self.pk})

