from django.db import models


# Create your models here.
class UserAudioInfo(models.Model):
   # audio = models.FileField(upload_to="audio/")
    word = models.CharField(max_length=100)
    streak = models.IntegerField()