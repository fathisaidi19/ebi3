# annonces/forms.py
from django import forms
from django.forms.models import inlineformset_factory
from .models import Annonce, PhotoAnnonce
from transporteurs.models import TransporteurProfile
from stockages.models import LieuStockageProfile

# Helper pour gérer les types de widgets (pour les templates)
try:
    from django_widget_tweaks.utils import field_type
except ImportError:
    # Fallback minimal si django_widget_tweaks n'est pas installé
    def field_type(field, type_name):
        return field.field.widget.__class__.__name__ == type_name


class AnnonceForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification d'une annonce,
    incluant la logique conditionnelle pour la sélection de logistique.
    """

    # Nous redéfinissons les champs FK pour pouvoir les rendre non-requis au niveau du formulaire
    transporteur_choisi = forms.ModelChoiceField(
        queryset=TransporteurProfile.objects.all().order_by('nom_entreprise'),
        required=False,
        label="Transporteur choisi (si méthode 2 ou 3)",
        empty_label="--- Sélectionner un Transporteur ---"
    )
    lieu_stockage_choisi = forms.ModelChoiceField(
        queryset=LieuStockageProfile.objects.all().order_by('nom_lieu'),
        required=False,
        label="Lieu de Stockage choisi (si méthode 3)",
        empty_label="--- Sélectionner un Lieu de Stockage ---"
    )

    class Meta:
        model = Annonce
        fields = [
            'titre', 'description', 'prix', 'categorie', 'etat',
            'pays_depart', 'ville_depart', 'pays_arrivee', 'ville_arrivee', 'date_livraison_estimee',
            'methode_livraison', 'transporteur_choisi', 'lieu_stockage_choisi', 'paiement_requis'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'date_livraison_estimee': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'methode_livraison': "Méthode Logistique (impacte les choix ci-dessous)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if not field_type(self.fields[field], 'CheckboxInput'):
                self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        """ Validation conditionnelle des champs de logistique. """
        cleaned_data = super().clean()
        methode = cleaned_data.get('methode_livraison')
        transporteur = cleaned_data.get('transporteur_choisi')
        stockage = cleaned_data.get('lieu_stockage_choisi')

        # Logique de validation
        if methode == Annonce.LIVRAISON_TRANSPORT:
            if not transporteur:
                self.add_error('transporteur_choisi', "Un transporteur doit être sélectionné pour la méthode 2.")
            cleaned_data['lieu_stockage_choisi'] = None

        elif methode == Annonce.LIVRAISON_STOCKAGE_TRANSPORT:
            if not transporteur:
                self.add_error('transporteur_choisi', "Un transporteur doit être sélectionné pour la méthode 3.")
            if not stockage:
                self.add_error('lieu_stockage_choisi', "Un lieu de stockage doit être sélectionné pour la méthode 3.")

        elif methode == Annonce.LIVRAISON_DEPOS:
            cleaned_data['transporteur_choisi'] = None
            cleaned_data['lieu_stockage_choisi'] = None

        return cleaned_data


# Création du FormSet pour les photos
PhotoAnnonceFormSet = inlineformset_factory(
    Annonce,
    PhotoAnnonce,
    fields=('image', 'description', 'is_main'),
    extra=1,  # Montrer un champ de photo vide par défaut
    max_num=5,  # Limite à 5 photos au total
    can_delete=True
)