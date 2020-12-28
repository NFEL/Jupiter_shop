from django import template

# from restaurant.models import Product
from product.models import Product
from pardakht.models import Cart

register = template.Library()

@register.filter()
def add_to_cart(value):
    print(value)
    try:
        product_obj = Product.objects.get(id=value)
        print(product_obj)
    except:
        pass

@register.filter(is_safe=True)
def multi(value, arg):
    return value * arg
    # print(arg)
    

# @register.filter(is_safe=True)
# def comma_seperator(value, arg):
#     temp = []

#     while True:
#         temp.append(str(value % 1000))
#         value //= 1000
#         if not value:
#             break
#     temp = temp[::-1]

#     res = ",".join(temp)
#     return res


# @register.filter(is_safe=True)
# def select_user_from_email(value):
#     username = value.split('@')[0]
#     return username


# @register.simple_tag
# def get_object_by_name(data):
#     product = Product.objects.get(name=data)
#     suppliers = product.supplier.all()

#     temp = ''
#     for e in suppliers:
#         temp = temp + e.account.name + ' '

#     return temp


# @register.simple_tag()
# def multiply(qty, unit_price, *args, **kwargs):
#     # you would need to do any localization of the result here
#     return qty * unit_price
