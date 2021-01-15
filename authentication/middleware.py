from pardakht.views import CartDetailView
from django.utils.deprecation import MiddlewareMixin

from pardakht.models import Cart, CartItems
from product.models import Product
from product.views import Landing


class CartMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):

        assert hasattr(request, 'user'), "shalgham man bad az Auth middleweram"
        if request.user.is_authenticated:
            cart, status = Cart.objects.get_or_create(user=request.user)
            session_cart = request.session.get('cart', None)
            if session_cart != None:
                for item in session_cart:
                    try:
                        c = CartItems.objects.create(
                            product=Product.objects.get(id=item[0]),
                            cart=cart,
                            qty=item[1],
                        )
                    except:
                        pass
                print('Cleared cached cart for user')
                del request.session['cart']
            request.cart = cart
        else:
            if request.session.get('cart', 1) == 1:
                print('Empty cart created for Unauthorized user')
                request.session['cart'] = []

    def process_view(self, request, view_func, *args, **kwargs):

        # if view_func.__name__ in (Landing.__name__, CartDetailView.__name__):

        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            total_price = cart.my_price()
            cart_items = CartItems.objects.filter(cart=cart)

        else:
            cart_items = []
            total_price = 0
            for item in request.session.get('cart'):
                product_obj = Product.objects.get(id=item[0])
                total_price += product_obj.my_price() * item[1]
                cart_items.append({
                    'product':  product_obj,
                    'qty': item[1],
                })

        request.cart_items = cart_items
        request.cart_total = total_price

        return None
