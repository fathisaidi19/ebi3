# transporteurs/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class TransporteurProfile(models.Model):
    """
    Modèle représentant le profil détaillé d'une entreprise ou d'un individu transporteur.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='transporteur_profile',
        verbose_name="Utilisateur lié"
    )
    nom_entreprise = models.CharField(max_length=150, unique=True, verbose_name="Nom de l'Entreprise/Service")
    description = models.TextField(verbose_name="Description des services",
                                   help_text="Décrivez votre offre, votre expérience et vos garanties.")
    licence_transport = models.CharField(max_length=100, blank=True, null=True, verbose_name="Numéro de Licence/Permis")

    # Coordonnées / Localisation principale
    pays_base = models.CharField(max_length=50, verbose_name="Pays de base")
    ville_base = models.CharField(max_length=50, verbose_name="Ville principale")

    # Compétences et Services
    METHODES_CHOICES = [
        ('Route', 'Transport Routier (Voiture/Camion)'),
        ('Air', 'Fret Aérien'),
        ('Mer', 'Fret Maritime'),
        ('Autres', 'Autres (Course, Relais, etc.)'),
    ]
    methodes_transportees = models.CharField(
        max_length=10,
        choices=METHODES_CHOICES,
        default='Route',
        verbose_name="Méthode principale"
    )
    # Champ booléen pour les services spéciaux
    assurance_incluse = models.BooleanField(default=False, verbose_name="Assurance incluse par défaut")
    transport_dangereux = models.BooleanField(default=False, verbose_name="Transport de matières dangereuses autorisé")

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil Transporteur"
        verbose_name_plural = "Profils Transporteurs"

    def __str__(self):
        return self.nom_entreprise

    def get_absolute_url(self):
        return reverse('transporteur_detail', kwargs={'pk': self.pk})