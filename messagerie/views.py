# messagerie/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required  # ⬅️ NOUVELLE IMPORTATION
from django.contrib import messages
from django.db.models import Q
from django.db import models  # Importé pour models.Count

from annonces.models import Annonce
from .models import Conversation, Message
from .forms import MessageForm


# --- 1. LISTE DES CONVERSATIONS (Boîte de réception) ---
# Utilise toujours LoginRequiredMixin car c'est une Class-Based View
class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'messagerie/conversation_list.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by('-derniere_activite')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['non_lus_count'] = Message.objects.filter(
            conversation__participants=self.request.user,
            est_lu=False
        ).exclude(expediteur=self.request.user).count()
        return context


# --- 2. DÉTAIL DE LA CONVERSATION ET ENVOI DE MESSAGE ---
# Utilise toujours LoginRequiredMixin car c'est une Class-Based View
class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'messagerie/conversation_detail.html'
    context_object_name = 'conversation'

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.object

        # Marquer tous les messages non lus (de l'autre partie) comme lus
        messages_non_lus = conversation.messages.filter(est_lu=False).exclude(expediteur=self.request.user)
        messages_non_lus.update(est_lu=True)

        context['form'] = MessageForm()
        context['autre_participant'] = conversation.participants.exclude(id=self.request.user.id).first()

        return context

    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.expediteur = request.user
            message.save()

            conversation.derniere_activite = message.date_envoi
            conversation.save()

            return redirect('conversation_detail', pk=conversation.pk)

        context = self.get_context_data(object=conversation)
        context['form'] = form
        return render(request, self.template_name, context)


# --- 3. DÉMARRER UNE CONVERSATION (VUE CORRIGÉE) ---

@login_required  # ⬅️ UTILISATION CORRECTE DU DÉCORATEUR DE FONCTION
def start_conversation(request, user_id=None, annonce_pk=None):
    """
    Démarre ou redirige vers une conversation existante.
    """

    if user_id and int(user_id) == request.user.id:
        messages.error(request, "Vous ne pouvez pas démarrer une conversation avec vous-même.")
        return redirect('conversation_list')

    if user_id:
        autre_utilisateur = get_object_or_404(User, pk=user_id)
        participants_ids = sorted([request.user.id, autre_utilisateur.id])
    else:
        messages.error(request, "Impossible de démarrer la conversation sans destinataire.")
        return redirect('conversation_list')

    annonce = None
    if annonce_pk:
        annonce = get_object_or_404(Annonce, pk=annonce_pk)

    # Tenter de trouver une conversation existante
    conversation = Conversation.objects.filter(
        annonce=annonce,
        participants__in=[participants_ids[0]]
    ).filter(
        participants__in=[participants_ids[1]]
    ).annotate(
        # Compter que deux participants (l'utilisateur et l'autre) sont présents
        num_participants=models.Count('participants')
    ).filter(
        num_participants=2
    ).first()

    # Si la conversation existe, rediriger
    if conversation:
        return redirect('conversation_detail', pk=conversation.pk)

    # Sinon, créer une nouvelle conversation
    nouvelle_conversation = Conversation.objects.create(annonce=annonce)
    nouvelle_conversation.participants.add(request.user, autre_utilisateur)

    messages.success(request, f"Nouvelle conversation démarrée avec {autre_utilisateur.username}.")

    return redirect('conversation_detail', pk=nouvelle_conversation.pk)