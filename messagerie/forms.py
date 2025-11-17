# messagerie/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """
    Formulaire minimaliste pour envoyer un nouveau message.
    """
    class Meta:
        model = Message
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Écrivez votre message ici...',
                'class': 'form-control message-input'
            }),
        }
        labels = {
            'contenu': '' # Pas de label visible pour ce champ
        }