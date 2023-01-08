from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=100 , unique=True)
    type = models.CharField(max_length=2000)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
