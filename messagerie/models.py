# messagerie/models.py
from django.db import models
from django.contrib.auth import get_user_model
from annonces.models import Annonce  # Pour lier la conversation à une annonce spécifique

User = get_user_model()


class Conversation(models.Model):
    """
    Représente un fil de discussion unique entre plusieurs utilisateurs,
    souvent initié par rapport à une annonce spécifique.
    """
    annonce = models.ForeignKey(
        Annonce,
        related_name='conversations',
        on_delete=models.SET_NULL,  # Ne supprime pas la conversation si l'annonce est supprimée
        null=True,
        blank=True,
        verbose_name="Annonce associée"
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        verbose_name="Participants"
    )
    date_demarrage = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de démarrage"
    )
    derniere_activite = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Dernière activité"
    )

    class Meta:
        ordering = ('-derniere_activite',)
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        participants_noms = ", ".join([p.username for p in self.participants.all()])
        return f"Conv. {self.pk} ({participants_noms})"

    def update_last_activity(self):
        """ Met à jour le champ derniere_activite à chaque nouveau message. """
        self.derniere_activite = models.DateTimeField(auto_now=True)
        self.save()


class Message(models.Model):
    """
    Représente un message individuel au sein d'une conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE,
        verbose_name="Conversation"
    )
    expediteur = models.ForeignKey(
        User,
        related_name='messages_envoyes',
        on_delete=models.CASCADE,
        verbose_name="Expéditeur"
    )
    contenu = models.TextField(
        verbose_name="Contenu du message"
    )
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'envoi"
    )
    est_lu = models.BooleanField(
        default=False,
        verbose_name="Est lu"
    )

    class Meta:
        ordering = ('date_envoi',)
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message de {self.expediteur.username} ({self.date_envoi.strftime('%H:%M')})"