from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.cache import cache, utils


from .models import Cart, CartItems
from product.models import Product


def add_to_cart(request, id, *args, **kwargs):
    doing_stuff('add', request, id, *args, **kwargs)
    if request.GET.get('next'):
        return redirect(request.GET.get('next')) 
    return redirect('categories')
    # return redirect(request.GET.get('next'))


def remove_from_cart(request, id, *args, **kwargs):
    doing_stuff('remove', request, id, *args, **kwargs)
    return redirect('cart')
    # return redirect(request.GET.get('next'))


def reduction_from_cart(request, id, *args, **kwargs):
    doing_stuff('sub', request, id, *args, **kwargs)
    return redirect('cart')
    # return redirect(request.GET.get('next'))


def set_qty_in_cart(request, id, *args, **kwargs):
    doing_stuff(request.POST.get('set-qty'), request, id, *args, **kwargs)
    return redirect('cart')
    # return redirect(request.GET.get('next'))


def do_wehave_enough(value, obj, p_obj):
    user_order=None
    if isinstance(obj, CartItems):
        user_order=obj.qty
    elif isinstance(obj, int):
        user_order=obj
    current_stock=p_obj.stock_count

    if value == 'add':
        value=1
        # if current_stock == 0 :
        #     return False
    if value == 'sub':
        value=-1
    # if isinstance(value, int):
    #     value = 0
    if user_order != None:
        return 0 <= user_order + value <= current_stock
    else:
        return False


def doing_stuff(op, request, id, *args, **kwargs):
    try:
        product_obj=Product.objects.get(id=id)
        if not request.user.is_anonymous:
            # request.cart.product.add(product_obj)
            product_item_in_cart, status=CartItems.objects.get_or_create(
                product=product_obj, cart=request.cart)
            qty=product_item_in_cart.qty
            if op == 'add' and do_wehave_enough(op, product_item_in_cart, product_obj):
                qty += 1

            if op == 'sub' and do_wehave_enough(op, product_item_in_cart, product_obj):
                qty -= 1
            if isinstance(op, int) and do_wehave_enough(op, product_item_in_cart, product_obj):
                product_item_in_cart.qty=op

            if op == 'remove' or qty == 0:
                product_item_in_cart.delete()
            else:
                product_item_in_cart.qty=qty

                product_item_in_cart.save()
        else:
            added=False
            new_list=request.session.get('cart')
            if op == 'remove':

                for i in range(len(new_list)):
                    item=new_list[i]
                    if product_obj.id == item[0]:
                        print(product_obj)
                        print(new_list)
                        del new_list[i]
                        print(new_list)
                        break
            else:
                for item in new_list:
                    if product_obj.id == item[0]:
                        added=True
                        if op == 'add' and do_wehave_enough(op, item[1], product_obj):
                            item[1] += 1
                        if op == 'sub' and do_wehave_enough(op, item[1], product_obj):
                            item[1] -= 1
                        if isinstance(op, int) and do_wehave_enough(op, item[1], product_obj):
                            item[1]=op

                        break
                if not added:
                    # if do_wehave_enough(op, 0, product_obj):
                    new_list.append([product_obj.id, 1],)

            request.session['cart']=new_list

        key=utils.make_template_fragment_key('landing-whole-page')
        try:
            cache.delete(key)
        except Exception as e:
            raise ValueError(e)
    except Exception as e:
        print(e)
        raise e


class CartDetailView(DetailView):

    template_name="cart.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # print(request.session['cart'])
        return render(request, "cart.html")

    def get_queryset(self):

        return
