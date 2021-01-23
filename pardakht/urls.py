from django.urls import path
from .views import add_to_cart,remove_from_cart,reduction_from_cart,set_qty_in_cart,CartDetailView,Checkout

urlpatterns = [
    path('add/<int:id>', add_to_cart, name='add-to-cart'),
    path('sub/<int:id>', reduction_from_cart, name='reduce-from-cart'),
    path('set/<int:id>', set_qty_in_cart, name='set-qty-in-cart'),
    path('remove/<int:id>', remove_from_cart, name='remove-from-cart'),

    path('checkout/', Checkout.as_view(), name='checkout'),
    path('', CartDetailView.as_view(), name='cart'),
]
