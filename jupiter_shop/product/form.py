from django import forms
from django.forms.models import ModelForm, fields_for_model

from .models import Category,SubCategory

class AddCategory(ModelForm):
    class Meta:
        model = Category
        fields = fields_for_model(Category)

class AddSubCategory(ModelForm):
    its_category = forms.ModelChoiceField(SubCategory.objects.all())
    class Meta:
        model = Category
        fields = ['title','description','image','its_category']
