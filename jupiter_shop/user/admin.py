from django.contrib import admin

# Register your models here.
from .models import Profile, User

admin.site.register(User)
admin.site.register(Profile)