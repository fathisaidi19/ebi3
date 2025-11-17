# messagerie/admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe  # Nécessaire pour afficher le HTML dans annonce_lien
from .models import Conversation, Message


# Inline pour les messages
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    # Correction de 'timestamp', utilise les bons noms de champs
    readonly_fields = ('expediteur', 'date_envoi', 'contenu', 'est_lu')
    fields = ('expediteur', 'contenu', 'date_envoi', 'est_lu')
    can_delete = False


# Admin pour Conversation
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    # Correction de 'starter', 'recipient', 'last_message_at'
    list_display = ('__str__', 'annonce_lien', 'display_participants', 'derniere_activite')
    # Correction de 'last_message_at', 'starter', 'recipient'
    list_filter = ('derniere_activite', 'date_demarrage', 'annonce')
    search_fields = ('annonce__titre', 'participants__username')
    # Correction de 'last_message_at'
    readonly_fields = ('date_demarrage', 'derniere_activite', 'annonce_lien')
    inlines = [MessageInline]
    filter_horizontal = ('participants',)

    # Méthodes personnalisées pour l'affichage dans l'Admin
    def display_participants(self, obj):
        # Affiche tous les participants séparés par une virgule
        return ", ".join([p.username for p in obj.participants.all()])

    display_participants.short_description = 'Participants'

    def annonce_lien(self, obj):
        if obj.annonce:
            # Crée un lien vers l'annonce dans l'admin
            url = reverse("admin:annonces_annonce_change", args=[obj.annonce.pk])
            return mark_safe(f'<a href="{url}">{obj.annonce.titre}</a>')
        return "N/A"

    annonce_lien.short_description = 'Annonce'

    fieldsets = (
        (None, {
            'fields': ('annonce', 'participants')
        }),
        ('Historique', {
            'fields': ('date_demarrage', 'derniere_activite'),
        })
    )


# Admin pour Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Correction de 'sender', 'timestamp', 'is_read'
    list_display = ('conversation', 'expediteur', 'contenu', 'date_envoi', 'est_lu')
    # Correction de 'is_read', 'timestamp'
    list_filter = ('est_lu', 'date_envoi', 'conversation')
    search_fields = ('contenu', 'expediteur__username', 'conversation__annonce__titre')
    # Correction de 'timestamp'
    readonly_fields = ('date_envoi', 'est_lu')

    # Assurez-vous d'importer reverse pour la méthode annonce_lien
    from django.urls import reverse