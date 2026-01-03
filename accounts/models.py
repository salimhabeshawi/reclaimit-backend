from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, telegram_username, password=None, **extra_fields):
        if not telegram_username:
            raise ValueError("The Telegram username must be set")
        if not telegram_username.startswith("@"):
            raise ValueError("Telegram username must start with '@'")
        user = self.model(telegram_username=telegram_username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(telegram_username, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    username = None

    telegram_username = models.CharField(
        max_length=32,
        unique=True,
        validators=[
            RegexValidator(
                regex="^@",
                message="Telegram username must start with '@'",
            )
        ],
    )
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    USERNAME_FIELD = "telegram_username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.telegram_username
