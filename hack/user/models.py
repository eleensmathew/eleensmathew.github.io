from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
# Create your models here.
class storage(models.Model):
    video=models.FileField(upload_to='videos_uploaded',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    date_uploaded = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to='images_uploaded',null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.TextField()
    audio=models.FileField(upload_to='audios_uploaded',null=True,validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    def time(self):
        return self.date_uploaded
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)