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
import random
import json
from django.http import JsonResponse
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
    
    

   # 3 letras o menos     
easy_words = ['cat', 'dog', 'sun', 'run', 'big', 'red', 'sky', 'fox', 'cup', 'box', 
         'hat', 'hot', 'fly', 'fan', 'bed', 'bug', 'pen', 'fun', 'ice', 'pie',
         'joy', 'cry', 'win', 'sad', 'top', 'cow', 'fox', 'bat', 'mat', 'son',
         'map', 'tap', 'wet', 'dry', 'gem', 'jam', 'mix', 'fix', 'fig', 'pig',
         'oil', 'ink', 'cut', 'bus', 'egg', 'zap', 'zip', 'axe', 'job', 'web',
         'yes', 'no', 'jam', 'jet', 'lot', 'let', 'jet', 'let', 'log', 'peg',
         'mud', 'bug', 'rug', 'toy', 'tip', 'lip', 'bus', 'dip', 'lip', 'bus',
         'fit', 'bit', 'kit', 'pit', 'hit', 'wit', 'yet', 'set', 'pet', 'net',
         'wet', 'vet', 'hex', 'hop', 'pop', 'jot', 'lot', 'cot', 'cut', 'but',
         'nut', 'hot', 'dot', 'pot', 'rob', 'sob', 'nod', 'rod', 'cod', 'lid']
# entre 4 y 7 letras
medium_words = ['apple', 'banana', 'orange', 'peach', 'grape', 'melon', 'lemon', 'cherry', 'kiwi', 'mango',
         'carrot', 'potato', 'tomato', 'onion', 'celery', 'spinach', 'pepper', 'cabbage', 'radish', 'turnip',
         'chicken', 'turkey', 'rabbit', 'donkey', 'monkey', 'giraffe', 'penguin', 'elephant', 'rhinoceros', 'alligator',
         'school', 'college', 'library', 'hospital', 'airport', 'station', 'factory', 'bakery', 'pharmacy', 'restaurant',
         'table', 'chair', 'sofa', 'couch', 'shelf', 'mirror', 'radio', 'laptop', 'tablet', 'camera',
         'purple', 'yellow', 'orange', 'green', 'brown', 'black', 'white', 'silver', 'golden', 'violet',
         'summer', 'winter', 'spring', 'autumn', 'morning', 'evening', 'afternoon', 'midnight', 'twilight', 'sunrise',
         'hockey', 'tennis', 'soccer', 'basketball', 'baseball', 'football', 'volleyball', 'badminton', 'swimming', 'wrestling',
         'mountain', 'valley', 'river', 'ocean', 'forest', 'desert', 'island', 'canyon', 'plain', 'plateau']
# 8 letras o mas
hard_words = ['computer', 'elephant', 'telephone', 'marketing', 'beautiful', 'wonderful', 'universe', 'challenge', 'happiness', 'community',
         'important', 'delicious', 'mysterious', 'fantastic', 'education', 'knowledge', 'tremendous', 'adventure', 'celebrate', 'celebrity',
         'technology', 'generation', 'experience', 'enthusiasm', 'television', 'revolution', 'agriculture', 'astronomy', 'butterfly', 'celestial',
         'chocolate', 'direction', 'discovery', 'evaluation', 'leadership', 'literature', 'management', 'meditation', 'motivation', 'navigation',
         'opportunity', 'photography', 'psychology', 'reflection', 'remarkable', 'restaurant', 'successful', 'sustainability', 'university', 'vacation',
         'imagination', 'communication', 'conversation', 'information', 'championship', 'determination', 'relationship', 'professional', 'recognition', 'organization',
         'architecture', 'celebration', 'competition', 'entertainment', 'intelligence', 'possibility', 'resilience', 'satisfaction', 'significant', 'temperature',
         'acceleration', 'celebratory', 'collaboration', 'development', 'environment', 'extraordinary', 'opportunities', 'participation', 'relationship', 'transformation',
         'communication', 'entertainment', 'international', 'organization', 'responsibility', 'unprecedented', 'disappointment', 'infrastructure', 'understanding', 'consideration']


def RandomWord(difficulty):
    word = ""
    if(difficulty == "easy"):
        word = random.choice(easy_words)
    elif(difficulty == "medium"):
        word = random.choice(medium_words)
    elif(difficulty == "hard"):
        word = random.choice(hard_words)
    else: 
        print("Dicha dificultad no esta configurada")
    return word

easy_words = ['cat', 'dog', 'sun', 'run', 'big', 'red', 'sky', 'fox', 'cup', 'box', 
         'hat', 'hot', 'fly', 'fan', 'bed', 'bug', 'pen', 'fun', 'ice', 'pie',
         'joy', 'cry', 'win', 'sad', 'top', 'cow', 'fox', 'bat', 'mat', 'son',
         'map', 'tap', 'wet', 'dry', 'gem', 'jam', 'mix', 'fix', 'fig', 'pig',
         'oil', 'ink', 'cut', 'bus', 'egg', 'zap', 'zip', 'axe', 'job', 'web',
         'yes', 'no', 'jam', 'jet', 'lot', 'let', 'jet', 'let', 'log', 'peg',
         'mud', 'bug', 'rug', 'toy', 'tip', 'lip', 'bus', 'dip', 'lip', 'bus',
         'fit', 'bit', 'kit', 'pit', 'hit', 'wit', 'yet', 'set', 'pet', 'net',
         'wet', 'vet', 'hex', 'hop', 'pop', 'jot', 'lot', 'cot', 'cut', 'but',
         'nut', 'hot', 'dot', 'pot', 'rob', 'sob', 'nod', 'rod', 'cod', 'lid']
# entre 4 y 7 letras
medium_words = ['apple', 'banana', 'orange', 'peach', 'grape', 'melon', 'lemon', 'cherry', 'kiwi', 'mango',
         'carrot', 'potato', 'tomato', 'onion', 'celery', 'spinach', 'pepper', 'cabbage', 'radish', 'turnip',
         'chicken', 'turkey', 'rabbit', 'donkey', 'monkey', 'giraffe', 'penguin', 'elephant', 'rhinoceros', 'alligator',
         'school', 'college', 'library', 'hospital', 'airport', 'station', 'factory', 'bakery', 'pharmacy', 'restaurant',
         'table', 'chair', 'sofa', 'couch', 'shelf', 'mirror', 'radio', 'laptop', 'tablet', 'camera',
         'purple', 'yellow', 'orange', 'green', 'brown', 'black', 'white', 'silver', 'golden', 'violet',
         'summer', 'winter', 'spring', 'autumn', 'morning', 'evening', 'afternoon', 'midnight', 'twilight', 'sunrise',
         'hockey', 'tennis', 'soccer', 'basketball', 'baseball', 'football', 'volleyball', 'badminton', 'swimming', 'wrestling',
         'mountain', 'valley', 'river', 'ocean', 'forest', 'desert', 'island', 'canyon', 'plain', 'plateau']
# 8 letras o mas
hard_words = ['computer', 'elephant', 'telephone', 'marketing', 'beautiful', 'wonderful', 'universe', 'challenge', 'happiness', 'community',
         'important', 'delicious', 'mysterious', 'fantastic', 'education', 'knowledge', 'tremendous', 'adventure', 'celebrate', 'celebrity',
         'technology', 'generation', 'experience', 'enthusiasm', 'television', 'revolution', 'agriculture', 'astronomy', 'butterfly', 'celestial',
         'chocolate', 'direction', 'discovery', 'evaluation', 'leadership', 'literature', 'management', 'meditation', 'motivation', 'navigation',
         'opportunity', 'photography', 'psychology', 'reflection', 'remarkable', 'restaurant', 'successful', 'sustainability', 'university', 'vacation',
         'imagination', 'communication', 'conversation', 'information', 'championship', 'determination', 'relationship', 'professional', 'recognition', 'organization',
         'architecture', 'celebration', 'competition', 'entertainment', 'intelligence', 'possibility', 'resilience', 'satisfaction', 'significant', 'temperature',
         'acceleration', 'celebratory', 'collaboration', 'development', 'environment', 'extraordinary', 'opportunities', 'participation', 'relationship', 'transformation',
         'communication', 'entertainment', 'international', 'organization', 'responsibility', 'unprecedented', 'disappointment', 'infrastructure', 'understanding', 'consideration']


def RandomWord(difficulty):
    word = ""
    if(difficulty == "easy"):
        word = random.choice(easy_words)
    elif(difficulty == "medium"):
        word = random.choice(medium_words)
    elif(difficulty == "hard"):
        word = random.choice(hard_words)
    else: 
        print("Dicha dificultad no esta configurada")
    return word

@csrf_exempt
def random_word(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            difficulty = data.get('difficulty')
            if difficulty in ["easy", "medium", "hard"]:
                word = RandomWord(difficulty)
                return JsonResponse({'word': word})
            else:
                return JsonResponse({'error': 'Dificultad no válida'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos no válidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
        
        
    