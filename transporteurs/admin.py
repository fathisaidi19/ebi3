# transporteurs/admin.py
from django.contrib import admin
from .models import TransporteurProfile

@admin.register(TransporteurProfile)
class TransporteurProfileAdmin(admin.ModelAdmin):
    list_display = ('nom_entreprise', 'user', 'pays_base', 'ville_base', 'methodes_transportees', 'assurance_incluse')
    list_filter = ('methodes_transportees', 'assurance_incluse', 'transport_dangereux')
    search_fields = ('nom_entreprise', 'description', 'user__username')