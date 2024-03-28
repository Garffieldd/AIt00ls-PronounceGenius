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

# Create your views here.



class LoadInputDataView(APIView):
    parser_classes = (MultiPartParser,)
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print("llegooooo",request.data)  # Aquí puedes procesar el archivo de audio
        return Response({'message': 'Archivo recibido correctamente'}, status=status.HTTP_201_CREATED)
    
    

class UserAudioInfoViewSet(viewsets.ModelViewSet):
    queryset = UserAudioInfo.objects.all()
    serializer_class = UserAudioInfoSerializer
