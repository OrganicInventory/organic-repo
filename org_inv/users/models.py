from django.db import models
from django.contrib.auth.models import User, AnonymousUser

# Create your models here.

class Profile(models.Model):
    location = models.CharField(max_length=255, null=True, blank=True)
    spa_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=15)
    threshold = models.IntegerField(null=True, default=30)
    user = models.OneToOneField(User, null=True)

    def __str__(self):
        return str(self.user)

def get_profile(user, save=False):
    if type(user) == AnonymousUser:
        return None
    else:
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile()
            profile.user = user
            if save: profile.save()
        finally:
            return profile
