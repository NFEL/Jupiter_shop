from django import forms
from django.contrib.gis.geos import Point
from .models import UserAddress
from leaflet.forms.widgets import LeafletWidget



class UserLocationMarker(forms.ModelForm):

    starting_location = (32.24997445586331, 53.61328125000001)
    
    class Meta:
        model = UserAddress
        fields = '__all__'
        widgets = {'location': LeafletWidget(),}

