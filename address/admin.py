from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin


from .models import StoreAddress, UserAddress

admin.site.register(UserAddress, LeafletGeoAdmin)
admin.site.register(StoreAddress, LeafletGeoAdmin)
