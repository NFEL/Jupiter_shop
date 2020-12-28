from django.contrib import admin

from .models import Social ,Payment ,Cart,Purchases,CartItems

    
class CartItemss(admin.StackedInline):
    model = CartItems

class CartItemssInline(admin.ModelAdmin):
    inlines = [
        CartItemss
    ]




admin.site.register(Social)
admin.site.register(Payment)
admin.site.register(Cart,CartItemssInline)
# admin.site.register(CartItems)
admin.site.register(Purchases)

