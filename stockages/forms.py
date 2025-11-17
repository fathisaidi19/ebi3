# stockages/forms.py
from django import forms
from .models import LieuStockageProfile

class LieuStockageProfileForm(forms.ModelForm):
    """
    Formulaire pour créer et éditer le profil d'un Lieu de Stockage.
    """
    class Meta:
        model = LieuStockageProfile
        # 'user' est exclu car il est assigné automatiquement par la vue
        fields = [
            'nom_lieu', 'description', 'superficie_m2',
            'pays', 'ville', 'adresse_complete',
            'temperature_controle', 'securite_24_7'
        ]
        labels = {
            'nom_lieu': "Nom de votre lieu de stockage",
            'description': "Description des services de stockage (sécurité, accès, etc.)",
            'superficie_m2': "Superficie disponible (en m²)",
            'pays': "Pays de localisation",
            'ville': "Ville de localisation",
            'adresse_complete': "Adresse complète (pour référence interne/contrat)",
            'temperature_controle': "Stockage à température contrôlée",
            'securite_24_7': "Sécurité et surveillance 24/7",
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout de styles de formulaire de base
        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.CheckboxInput):
                self.fields[field].widget.attrs['class'] = 'form-control'