from django.db import models
import heapq
from django.core.validators import MaxValueValidator
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from PIL import Image 
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)
class CustomUser(AbstractUser):
    
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)

    USERNAME_FIELD = "email" # make the user log in with the email
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

class PriorityQueue(models.Model):
    data = models.JSONField(default=dict)

    def __init__(self, *args, **kwargs):    #initializing heap as an empty list
        super().__init__(*args, **kwargs)
        self.heap = []
        self._heapify()

    def __str__(self):
        return str(self.data)
    
    # def __lt__(self, other):
    #     return self.data.keys()[0] < other.data.keys()[0]

    def push(self, priority, value):
        heapq.heappush(self.heap, int(priority))
        if priority not in self.data:       #to avoid the overlapping of the values for which keys are same
            self.data[priority] = []
        self.data[priority].append(value)
        self.save()

    def pop(self):              #removes the value with highest priority
        if not self.heap:
            raise IndexError("Heap is empty")
        priority, values = self.heap[0]
        value = values.pop(0)
        if not values:
            del self.data[priority]
            heapq.heappop(self.heap)
        self.save()
        return value

    def peek(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        priority, values = self.heap[0]
        return values[0]

    def _heapify(self):     #populate the dictionary with data keys and values
        for priority, values in self.data.items():
            heapq.heappush(self.heap, int(priority))

    def total_values(self):
        total = 0
        for values in self.data.values():
            total += len(values)
        return total
    
    class Meta:
        verbose_name_plural = "Priority Queues"


class Admin_info(models.Model):
    user = models.OneToOneField('CustomUser',null =True, on_delete=models.SET_NULL)
    priority = models.OneToOneField("PriorityQueue", on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
