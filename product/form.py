from django import forms
from django.forms.models import ModelForm, fields_for_model

from .models import Category,SubCategory

class AddCategory(ModelForm):
    class Meta:
        model = Category
        fields = fields_for_model(Category)



