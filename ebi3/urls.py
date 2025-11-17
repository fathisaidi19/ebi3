# ebi3/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ------------------ AUTHENTIFICATION ------------------
    path('comptes/', include('comptes.urls')),
    path('comptes/', include('django.contrib.auth.urls')),

    # ------------------ ANNONCES ET MESSAGERIE ------------------
    path('', include('annonces.urls')),
    path('messagerie/', include('messagerie.urls')),

    # ------------------ LOGISTIQUE ------------------
    # URLs pour la gestion des transporteurs
    path('transporteurs/', include('transporteurs.urls')),  # ⬅️ AJOUTÉ
    # URLs pour la gestion des lieux de stockage
    path('stockages/', include('stockages.urls')),  # ⬅️ AJOUTÉ
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)