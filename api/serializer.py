from rest_framework import serializers
from .models import UserAudioInfo

class UserAudioInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserAudioInfo
        #fields=('word','streak')
        fields='__all__'