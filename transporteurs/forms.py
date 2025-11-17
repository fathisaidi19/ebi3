# transporteurs/forms.py
from django import forms
from .models import TransporteurProfile

class TransporteurProfileForm(forms.ModelForm):
    """
    Formulaire pour créer et éditer le profil d'un Transporteur.
    """
    class Meta:
        model = TransporteurProfile
        # 'user' est exclu car il est assigné automatiquement par la vue (CreateView)
        fields = [
            'nom_entreprise', 'description', 'licence_transport',
            'pays_base', 'ville_base', 'methodes_transportees',
            'assurance_incluse', 'transport_dangereux'
        ]
        labels = {
            'nom_entreprise': "Nom de votre service/entreprise de transport",
            'description': "Description de votre offre (expérience, garanties, etc.)",
            'licence_transport': "Numéro de Licence/Permis (Optionnel)",
            'pays_base': "Pays principal d'opération",
            'ville_base': "Ville principale d'opération",
            'methodes_transportees': "Méthode de transport principale",
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