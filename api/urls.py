from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserAudioInfoViewSet, LoadInputDataView, random_word, Recibir_correo_crear_progreso, delete_all_user_audio_info, obtener_todos_los_datos 

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
    path('delete_all/',delete_all_user_audio_info, name='delete_all'),
    #path('user_audio_info/recibir_correo/', UserAudioInfoViewSet.recibir_correo, name='recibir_correo'),
    path('recibir_correo/',Recibir_correo_crear_progreso, name='recibir_correo'),
    path('obtener/',obtener_todos_los_datos, name='obtener'),
    ]
    