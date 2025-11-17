# annonces/models.py

from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint, Q


# --- MODÈLE 1 : CATÉGORIE ---
# Utilisé pour le filtrage et l'organisation des annonces.
class Categorie(models.Model):
    """
    Modèle pour gérer les catégories et sous-catégories (arborescence).
    """
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la Catégorie")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sous_categories',
        verbose_name="Catégorie Parente"
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


# --- MODÈLES DE SERVICES LOGISTIQUES (Placeholders) ---
# Ces modèles représentent les entités auxquelles l'utilisateur peut faire appel (Choix 2 et 3)
# Ils seront liés à des profils utilisateurs dans une phase ultérieure.

class Transporteur(models.Model):
    """
    Représente une entreprise ou un individu capable d'assurer le transport.
    """
    nom_entreprise = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    # TODO: Ajouter une ForeignKey vers un modèle 'Profile' pour le lien utilisateur/notification.

    class Meta:
        verbose_name = "Transporteur"
        verbose_name_plural = "Transporteurs"

    def __str__(self):
        return self.nom_entreprise


class LieuStockage(models.Model):
    """
    Représente un lieu de stockage (entrepôt, etc.).
    """
    nom_lieu = models.CharField(max_length=255, unique=True)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)

    # TODO: Ajouter une ForeignKey vers un modèle 'Profile' pour le lien utilisateur/notification.

    class Meta:
        verbose_name = "Lieu de Stockage"
        verbose_name_plural = "Lieux de Stockage"

    def __str__(self):
        return f"{self.nom_lieu} ({self.ville})"


# --- MODÈLE 2 : ANNONCE ---

class Annonce(models.Model):
    # -- Propriétaire de l'Annonce (Dépositaire)
    depositaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='annonces_deposees'
    )

    # -- Champs Obligatoires
    titre = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)

    # État (Condition) Choices
    ETAT_CHOICES = [
        ('NEUF', 'Neuf'),
        ('COMME_NEUF', 'Utilisé mais comme neuf'),
        ('UTILISE', 'Utilisé'),
    ]
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='UTILISE')

    # -- Localisation (Itinéraire)
    pays_depart = models.CharField(max_length=100, verbose_name="Pays de Départ (A)")
    ville_depart = models.CharField(max_length=100, verbose_name="Ville de Départ (A)")
    pays_arrivee = models.CharField(max_length=100, verbose_name="Pays d'Arrivée (B)")
    ville_arrivee = models.CharField(max_length=100, verbose_name="Ville d'Arrivée (B)")
    date_livraison_estimee = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de livraison estimée"
    )

    # -- Méthode de Livraison
    LIVRAISON_CHOICES = [
        ('1', 'Dépositaire s\'occupe du transport'),
        ('2', 'Utilisation d\'un Transporteur (Choix dans la liste)'),
        ('3', 'Utilisation d\'un Lieu de Stockage + Transporteur'),
    ]
    methode_livraison = models.CharField(
        max_length=1,
        choices=LIVRAISON_CHOICES,
        default='1',
        verbose_name="Méthode Logistique"
    )

    # -- Liens aux Services Choisi (Uniquement si methode_livraison est 2 ou 3)
    transporteur_choisi = models.ForeignKey(
        Transporteur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    lieu_stockage_choisi = models.ForeignKey(
        LieuStockage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # -- Paiement (Flag pour les formules 1 et 2 nécessitant un paiement)
    paiement_requis = models.BooleanField(
        default=False,
        verbose_name="Paiement requis pour la logistique"
    )

    # -- Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"

    def __str__(self):
        return f"Annonce #{self.id}: {self.titre}"


# --- MODÈLE 3 : PHOTO/VIDÉO DE L'ANNONCE ---
# Gère le contenu multimédia (1 obligatoire, N optionnels)

class PhotoAnnonce(models.Model):
    """
    Modèle pour gérer les photos associées à une annonce.
    """
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='photos')
    # Utilisez FileField si vous voulez aussi accepter des vidéos.
    image = models.ImageField(upload_to='annonces/images/', verbose_name="Fichier Média")
    is_main = models.BooleanField(default=False, verbose_name="Photo Principale (Obligatoire)")
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Photo de l'Annonce"
        verbose_name_plural = "Photos des Annonces"
        # Contrainte pour s'assurer qu'une seule photo est marquée comme "Principale" (obligatoire)
        constraints = [
            # La contrainte Q(is_main=True) n'est pas supportée pour garantir qu'une seule photo
            # soit marquée 'is_main=True' par annonce, mais elle garantit la clé unique
            # si l'on tente d'insérer plusieurs fois la même annonce avec is_main=True.
            UniqueConstraint(fields=['annonce'], condition=Q(is_main=True), name='unique_main_photo_par_annonce')
        ]

    def __str__(self):
        return f"Média pour {self.annonce.titre}"


from django.db import models

# Create your models here.
