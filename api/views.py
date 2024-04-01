from django.shortcuts import render
from rest_framework import viewsets
from .serializer import UserAudioInfoSerializer
from .models import UserAudioInfo, Trys
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
import soundfile as sf
from django.http import HttpResponse

# Create your views here.



class LoadInputDataView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        if 'audio' not in request.FILES:
            print("No llego")
            return Response({'error': 'No se proporcionó ningún archivo de audio'}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = request.FILES['audio']
        word = request.data.get('word', '').strip()
        correo = request.data.get('correo')
        posible_nueva_racha = int(request.data.get('racha'))
        print("Llego")

        # Verificar la extensión del archivo
        if not audio_file.name.endswith('.mp3'):
            print("no es")
            return Response({'error': 'El archivo debe tener una extensión .mp3'}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir MP3 a WAV
        print("si es")
        with sf.SoundFile(audio_file) as mp3_audio:
            wav_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')
            sf.write(wav_path, mp3_audio.read(), mp3_audio.samplerate, format='WAV')
            print("1")

        # Reconocimiento de voz
        recognizer = sr.Recognizer()
        print("2")
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            print("3")

        try:
            # Reconocer texto
            print("4")
            recognized_text = recognizer.recognize_google(audio_data, language="en-US")
            
            print(recognized_text)
             # Comparar la palabra reconocida con la proporcionada
            if recognized_text.strip() == word:
                
                #correo = "sebastian_garfield18@ejemplo.com"
                TRY = Trys.objects.create(word= recognized_text.strip(), pronunciation=word,correct=True)
                UserAudioInfo_instance  = UserAudioInfo.objects.filter(email=correo).first()
                UserAudioInfo_instance.trys.add(TRY)
                #posible_nueva_racha = 5
                if UserAudioInfo_instance.max_streak < posible_nueva_racha:
                    UserAudioInfo_instance.max_streak = posible_nueva_racha
                    UserAudioInfo_instance.save()
                return Response({'status': 'correcto', 'text': recognized_text}, status=status.HTTP_200_OK)
            else:
                TRY = Trys.objects.create(word= recognized_text.strip(), pronunciation=word,correct=False)
                #correo = "sebastian_garfield18@ejemplo.com"
                UserAudioInfo_instance  = UserAudioInfo.objects.filter(email=correo).first()
                UserAudioInfo_instance.trys.add(TRY)
                #posible_nueva_racha = 5
                if UserAudioInfo_instance.max_streak < posible_nueva_racha:
                    UserAudioInfo_instance.max_streak = posible_nueva_racha
                    UserAudioInfo_instance.save()
                return Response({'status': 'incorrecto', 'text': recognized_text}, status=status.HTTP_200_OK)

        except sr.UnknownValueError:
            print("5")
            return Response({'error': 'No se pudo reconocer el texto del audio'}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError:
            print("6")
            return Response({'error': 'Error en la conexión con el servicio de reconocimiento de voz'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Eliminar el archivo WAV después de su uso
            os.remove(wav_path)
    
    

class UserAudioInfoViewSet(viewsets.ModelViewSet):
    queryset = UserAudioInfo.objects.all()
    serializer_class = UserAudioInfoSerializer
    """
    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'])
    def recibir_correo(self, request):
        correo = request.data.get('correo')
        # Aquí puedes procesar el correo electrónico como lo necesites
        print('Correo electrónico recibido:', correo)
        UserAudioInfo.objects.create(email=correo, word='', streak=0)
        return Response({'mensaje': 'Correo electrónico recibido correctamente'})
    """
    
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
    
    
@csrf_exempt
def Recibir_correo_crear_progreso(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        correo = data.get('correo')
        UserAudioInfo.objects.create(email=correo, max_streak=0)
        return JsonResponse({'mensaje': 'Correo electrónico recibido correctamente'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
        
    
@csrf_exempt
def delete_all_user_audio_info(request):
    if request.method == 'POST':
        # Borra todos los registros de UserAudioInfo
        UserAudioInfo.objects.all().delete()
        return HttpResponse("Todos los registros de UserAudioInfo han sido eliminados correctamente.")
    else:
        return render(request, 'delete_confirm.html')  # Muestra un mensaje de confirmación de eliminación
    
    
@csrf_exempt
def obtener_todos_los_datos(request):
    if request.method == 'GET':
        
        usuarios = UserAudioInfo.objects.all()

        
        datos_usuarios = []

        
        for usuario in usuarios:
            
            trys_usuario = usuario.trys.all().values('word', 'pronunciation', 'correct')

           
            datos_usuario = {
                'id': usuario.id,
                'email': usuario.email,
                'max_streak': usuario.max_streak,
                'trys': list(trys_usuario)
            }

           
            datos_usuarios.append(datos_usuario)

        
        return JsonResponse({'datos_usuarios': datos_usuarios})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)