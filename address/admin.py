from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin


from .models import Address

admin.site.register(Address,LeafletGeoAdmin)
