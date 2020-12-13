from django.db.models import query
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import Category, Product, SubCategory
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin





class Landing(LoginRequiredMixin, ListView):
    login_url= '/admin/'
    model = Category


    def get(self,request,*args, **kwargs):

        for ar in args:
            print(ar)

        print(kwargs)

        print(request.user.has_perm('product.view_product'))

        if request.user.has_perm('product.delete_product'):
            print("to mitoni")

        # print(type(request.GET.get('as')))
        return super().get(self,request,args,kwargs)



class SubCategories(ListView):
    model = SubCategory

    def get_queryset(self):

        category_obj = get_object_or_404(
            Category, title=self.request.GET.get('category', None))
        queryset = SubCategory.objects.filter(its_category=category_obj)

        return queryset


class Products(ListView):

    model = Product


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

    def get_queryset(self):

        sub_category_obj = get_object_or_404(
            SubCategory, title=self.request.GET.get('sub-category', None))

        queryset = Product.objects.filter(sub_category=sub_category_obj)
        for q in queryset:
            print(q)
        return queryset

class ProductDetail(DetailView):
    model = Product
    


class AllProducts(ListView):

    model = Product

    def get_queryset(self):
        category_obj = get_object_or_404(
            Category, title=self.request.GET.get('title', None))
        query_set = category_obj.sub_category_set.all()
        return query_set
