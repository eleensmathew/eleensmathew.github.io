from django.db import models
# Create your models here.
    
class Admin_info(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)
    priorityq = models.JSONField(default={})
    size = models.IntegerField(default=0)
    def __str__(self):
        return self.username