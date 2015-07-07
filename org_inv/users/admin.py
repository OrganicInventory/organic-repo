from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'spa_name', 'phone_number', 'location']

# Register your models here.

admin.site.register(Profile, ProfileAdmin)
