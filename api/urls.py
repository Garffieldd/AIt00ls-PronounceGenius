from django.urls import path,include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'user_audio_info',views.UserAudioInfoViewSet,basename='user_audio_info')
router.register(r'audio',views.UserAudioInfoViewSet,basename='audio')

urlpatterns= [
    path('',include(router.urls))
]