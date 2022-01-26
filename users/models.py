
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  email = models.EmailField("email address", unique=True)
  class Meta:
    db_table = "Users"
