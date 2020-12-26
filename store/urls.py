from django.urls import path

from .views import show_stores

urlpatterns = [
    path('', show_stores,name ='show_stores')
]
