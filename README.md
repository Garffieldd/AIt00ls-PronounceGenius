# AIt00ls-PronounceGenius
Aplicacion de reconocimiento de voz para pronunciar palabras en ingles



#Correr la base de datos

docker build -t django-postgres-image .
docker run -d --name django-postgres-container -p 5432:5432 django-postgres-image

