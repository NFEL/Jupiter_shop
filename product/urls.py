from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import  SubCategories, Products, Landing, get_price


urlpatterns = [
    path('', Landing.as_view(), name='categories'),
    path('<str:category>', SubCategories.as_view(), name='sub-categories'),
    path('products/', Products.as_view(), name='products'),
    path('price/<int:product_id>', get_price, name='product-price'),
]
