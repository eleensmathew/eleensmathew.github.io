from django.db import models

# Create your models here.


    
class Admin_info(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)
    #priority = models.ForeignKey(Priority,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
    
class Priority(models.Model):
    pq=models.IntegerField() #holds the priority of the video in the database
    pk_value=models.IntegerField(default=0) #used for getting the referrence no of the video
    admin_associated = models.ForeignKey(Admin_info,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pq)