from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
import os

def get_upload_to(instance, filename):
    return os.path.join('videos', str(instance.pk), filename)

class storage(models.Model):
    video=models.FileField(upload_to='videos_uploaded',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    date_uploaded = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to='images_uploaded',null=True)
    name = models.CharField(max_length=255, default=None)
    slug = models.SlugField(unique=True)
    location = models.TextField(default=None)
    audio=models.FileField(upload_to='audios_uploaded',null=True,validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    slug = models.SlugField(blank=True, unique=True)
    
    def time(self):
        return self.date_uploaded
    
    def get_absolute_url(self):
        return f"/products/{self.slug}/"
    
    def save(self, *args, **kwargs):
        self.video_file.name = self.get_unique_filename(self.video_file.name)
        super(Video, self).save(*args, **kwargs)

    def get_unique_filename(self, filename):
        name, ext = os.path.splitext(filename)
        slug = slugify(name)
        new_filename = f"{slug}{ext}"
        if Video.objects.filter(video_file__endswith=new_filename).exists():
            return self.get_unique_filename(f"{slug}-{Video.objects.count()}{ext}")
        return new_filename