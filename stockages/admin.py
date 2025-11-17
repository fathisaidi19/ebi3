# stockages/admin.py
from django.contrib import admin
from .models import LieuStockageProfile

@admin.register(LieuStockageProfile)
class LieuStockageProfileAdmin(admin.ModelAdmin):
    list_display = ('nom_lieu', 'user', 'ville', 'pays', 'superficie_m2', 'securite_24_7')
    list_filter = ('securite_24_7', 'temperature_controle')
    search_fields = ('nom_lieu', 'description', 'user__username', 'ville')