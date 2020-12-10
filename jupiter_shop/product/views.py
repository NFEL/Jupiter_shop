from django.db.models import query
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import Category, Product, SubCategory
from django.views.generic import ListView, DetailView


class Landing(ListView):
    model = Category

    def get_queryset(self):
        qs = Category.objects.all()
        for q in qs :
            print(q.image)
        return qs
    


class SubCategories(ListView):
    model = SubCategory

    def get_queryset(self):

        category_obj = get_object_or_404(
            Category, title=self.request.GET.get('category', None))
        queryset = SubCategory.objects.filter(its_category=category_obj)

        return queryset


class Products(ListView):

    model = Product

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

        # queryset = Product.objects.filter(sub_category_set = 'animals')
        return query_set
