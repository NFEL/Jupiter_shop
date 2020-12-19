from django.db.models import query
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Category, Product, SubCategory
from .form import AddCategory,AddSubCategory




class Landing( ListView):
    login_url= '/admin/'
    model = Category
    

    def post(self,request,*args, **kwargs):
        if request.user.has_perm('product.add_category'):
            form = AddCategory(data=request.POST,files= request.FILES)
            if form.is_valid():
                form.save()
        return redirect('categories')

class SubCategories(ListView):
    model = SubCategory

    def post(self,request,*args, **kwargs):
        current_category = kwargs.get('category')
        if request.user.has_perm('product.add_category'):
            sub_obj = SubCategory.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                its_category=get_object_or_404(Category,title=current_category),
                image=FileSystemStorage().save(f"{SubCategory.image.field.upload_to}/{request.FILES['image'].name}",request.FILES['image'])
                )
            

        return redirect('sub-categories',category=current_category)

    def save_my_image(self,file):
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        return fs.save(file.name, file)

    def get_queryset(self,*args, **kwargs):
        category_obj = get_object_or_404(
            Category, title=self.request.resolver_match.kwargs.get('category'))
        queryset = SubCategory.objects.filter(its_category=category_obj)
        return queryset



class Products(ListView):

    model = Product


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):

        sub_category_obj = get_object_or_404(
            SubCategory, title=self.request.GET.get('sub-category', None))

        queryset = Product.objects.filter(sub_category=sub_category_obj)
        
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
