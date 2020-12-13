from django.contrib import admin

# Register your models here.
from .models import Profile

# class AddressField(admin.TabularInline):


admin.site.register(Profile)