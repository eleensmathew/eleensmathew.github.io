from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
# Create your models here.
class storage(models.Model):
    video=models.FileField(upload_to='videos_uploaded',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    date_uploaded = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to='images_uploaded',null=True)
    audio=models.FileField(upload_to='audios_uploaded',null=True,validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    def time(self):
        return self.date_uploaded