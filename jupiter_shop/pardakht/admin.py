from django.contrib import admin

from .models import user , social , payment , purchase , order


admin.site.register(user)
admin.site.register(social)
admin.site.register(payment)
admin.site.register(purchase)
admin.site.register(order)

