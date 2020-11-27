from django.contrib import admin

# Register your models here.
from .models import Profile, User

# class AddressField(admin.TabularInline):


admin.site.register(User)
admin.site.register(Profile)