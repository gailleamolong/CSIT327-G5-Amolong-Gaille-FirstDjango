from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        ADMIN = 'ADMIN', 'Administrator'
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    course = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username