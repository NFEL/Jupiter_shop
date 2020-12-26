from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ProductDetail, SubCategories, AllProducts, Products, Landing, get_price


urlpatterns = [
    path('', Landing.as_view(), name='categories'),
    path('<str:category>', SubCategories.as_view(), name='sub-categories'),
    path('products/', Products.as_view(), name='products'),
    path('products/productDetail/<int:pk>',
         ProductDetail.as_view(), name='productDetail'),
    path('all/', AllProducts.as_view(), name='all-products'),
    path('p/<int:product_id>', get_price, name='product-price'),
]
