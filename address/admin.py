from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin


from .models import StoreAddress, UserAddress

admin.site.register(UserAddress)
admin.site.register(StoreAddress)
