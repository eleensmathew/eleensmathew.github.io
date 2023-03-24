from django.db import models
import jsonfield
# Create your models here.

class Priority(models.Model):
    pq = jsonfield.JSONField(default=[])
    def __str__(self):
        return str(self.pq)
    
class Admin_info(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)
    priorityq = jsonfield.JSONField(default={})
    def __str__(self):
        return self.username