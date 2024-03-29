from django.shortcuts import render
from rest_framework import viewsets
from .serializer import UserAudioInfoSerializer
from .models import UserAudioInfo
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from pydub import AudioSegment
import speech_recognition as sr
import os

# Create your views here.



class LoadInputDataView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        if 'audio_file' not in request.FILES:
            return Response({'error': 'No se proporcionó ningún archivo de audio'}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = request.FILES['audio_file']

        # Verificar la extensión del archivo
        if not audio_file.name.endswith('.mp3'):
            return Response({'error': 'El archivo debe tener una extensión .mp3'}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir MP3 a WAV
        mp3_audio = AudioSegment.from_mp3(audio_file)
        wav_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')
        mp3_audio.export(wav_path, format='wav')

        # Reconocimiento de voz
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        try:
            # Reconocer texto
            recognized_text = recognizer.recognize_google(audio_data, language="es-ES")
            return Response({'text': recognized_text}, status=status.HTTP_200_OK)
        except sr.UnknownValueError:
            return Response({'error': 'No se pudo reconocer el texto del audio'}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError:
            return Response({'error': 'Error en la conexión con el servicio de reconocimiento de voz'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Eliminar el archivo WAV después de su uso
            os.remove(wav_path)
    
    

class UserAudioInfoViewSet(viewsets.ModelViewSet):
    queryset = UserAudioInfo.objects.all()
    serializer_class = UserAudioInfoSerializer
