# messagerie/templatetags/my_custom_tags.py
from django import template

register = template.Library()

@register.filter
def is_other_party(conversation_user, current_user):
    """
    Retourne l'autre utilisateur participant à la conversation.
    Utilisation: {{ conversation.starter|is_other_party:user }}
    """
    if conversation_user == current_user:
        # Si starter est l'utilisateur courant, l'autre partie est le recipient
        return conversation_user.received_conversations.filter(pk=conversation_user.pk).first().recipient
    else:
        # Si starter n'est PAS l'utilisateur courant, l'autre partie est le starter
        return conversation_user