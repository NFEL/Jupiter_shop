from django.contrib import admin

from .models import Category, SubCategory, Product, ProductBrand,ProductPrice,ProductImage

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductBrand)
admin.site.register(ProductPrice)
admin.site.register(ProductImage)
