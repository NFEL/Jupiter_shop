from django.urls import path
from .views import ProductDetail, SubCategories, AllProducts, Products, Landing
#from .views import send_json



urlpatterns= [
    # path('log/<int:user_id>',Categories.as_view())
    path('',Landing.as_view(),name='categories'),
    path('subcat/',SubCategories.as_view(), name='sub-categories'),
    path('subcat/products/',Products.as_view(), name='products'),
    path('subcat/products/productDetail/<int:pk>',ProductDetail.as_view(), name='productDetail'),
    path('all/',AllProducts.as_view(), name='all-products')
]