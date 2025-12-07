from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None
    
    telegram_username = models.CharField(max_length=32, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    USERNAME_FIELD = "telegram_username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.telegram_username