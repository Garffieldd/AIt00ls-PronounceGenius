from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserAudioInfoViewSet, LoadInputDataView, random_word

# Creamos un enrutador
router = DefaultRouter()

# Registramos la vista UserAudioInfoViewSet con su nombre base 'user_audio_info'
router.register(r'user_audio_info', UserAudioInfoViewSet, basename='user_audio_info')

# No registramos LoadInputDataView con el enrutador, ya que es una vista basada en API y no un viewset

urlpatterns = [
    # Incluimos las URL del enrutador
    path('', include(router.urls)),
    # Agregamos la URL para la vista LoadInputDataView
    path(r'audio/', LoadInputDataView.as_view(), name='audio'),
    path('random_word/', random_word, name='random_word'),
]