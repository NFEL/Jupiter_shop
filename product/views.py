from django import views
from django.db.models import query
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Category, Product, ProductBrand, ProductImage, SubCategory, ProductPrice
from .form import AddCategory


class Landing(ListView):
    login_url = '/admin/'
    model = Category

    def __init__(self, **kwargs) -> None:
        self.p_list = Product.objects.all()
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('product.add_category'):
            form = AddCategory(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
        return redirect('categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('search'):
            self.p_list = self.p_list.filter(
            name__contains=self.request.GET.get('search'))
        context['product_list'] = self.p_list
        return context


class SubCategories(ListView):
    model = SubCategory

    def __init__(self, **kwargs) -> None:
        self.p_list = Product.objects.all()
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        current_category = kwargs.get('category')
        if request.user.has_perm('product.add_category'):
            sub_obj = SubCategory.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                its_category=get_object_or_404(
                    Category, title=current_category),
                image=FileSystemStorage().save(
                    f"{SubCategory.image.field.upload_to}/{request.FILES['image'].name}", request.FILES['image'])
            )
        return redirect('sub-categories', category=current_category)

    def save_my_image(self, file):
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        return fs.save(file.name, file)

    def get_queryset(self, *args, **kwargs):
        category_obj = get_object_or_404(
            Category, title=self.request.resolver_match.kwargs.get('category'))
        queryset = SubCategory.objects.filter(its_category=category_obj)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        if self.request.GET.get('search'):
            self.p_list = self.p_list.filter(
                name__contains=self.request.GET.get('search'))
        context['product_list'] = self.p_list.filter(
            category__title=self.request.resolver_match.kwargs.get('category'))
        return context


class Products(ListView):

    model = Product

    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pbrands = ProductBrand.objects.all()

        # sub_category_obj = get_object_or_404(
        #     SubCategory, title=self.request.GET.get('sub-category', None))

        # ProductBrand.objects.select_related('')
        context['brands'] = ProductBrand.objects.all()
        return context

    def get_queryset(self):

        sub_category = self.request.GET.get('sub-category', None)
        category = self.request.GET.get('category', None)
        brand = self.request.GET.get('brand', None)

        queryset = Product.objects.all()

        if sub_category:
            queryset = Product.objects.filter(sub_category__title=sub_category)

        if category:
            queryset = Product.objects.filter(category__title=category)

        if brand:
            queryset = Product.objects.filter(brand__name=brand)

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


def get_price(request, product_id, *args, **kwargs):
    price = 0
    p_obj = get_object_or_404(Product, id=product_id)
    price = p_obj.productprice_set.all().order_by('-datetime__minute')[0].price
    return HttpResponse(price)
