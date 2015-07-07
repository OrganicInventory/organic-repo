from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    location = models.CharField(max_length=255, null=True, blank=True)
    spa_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(User, null=True)

    def __str__(self):
        return str(self.user)
