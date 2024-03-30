from django.db import models


class Trys(models.Model):
    word = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=100)
    correct = models.BooleanField()

    def __str__(self):
        return self.word

# Create your models here.
class UserAudioInfo(models.Model):
   # audio = models.FileField(upload_to="audio/")
    email = models.CharField(unique=True,null=False,max_length=40,verbose_name='email')
    trys = models.ManyToManyField(Trys)
    max_streak = models.IntegerField()
    
    def __str__(self):
      return f"{self.pk}"
    