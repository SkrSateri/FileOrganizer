from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 200)
    name = models.CharField(max_length = 20)
    surname = models.CharField (max_length = 20)
    isAdmin = models.BooleanField(default = False)
    isActive = models.BooleanField(default = False)
