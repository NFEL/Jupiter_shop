from django.contrib import admin

from .models import Category, SubCategory, Product, ProductBrand,ProductPrice,ProductImage


class PriceInline(admin.TabularInline):
    model = ProductPrice

    
class ProductImages(admin.StackedInline):
    model = ProductImage
    parent_model = Product

class ProductInlnes(admin.ModelAdmin):
    inlines = [
        PriceInline,ProductImages
    ]



admin.site.register(Product, ProductInlnes)
admin.site.register(Category)
admin.site.register(SubCategory)
