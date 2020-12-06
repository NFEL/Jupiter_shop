from django.shortcuts import render
# from django.views import View
from product.models import Category 
from django.views.generic import ListView



    # def get(self, request):
    #     context = {}
    #     tmp = []
    #     all_cats = Category.objects.all()
        
    #     for cat in all_cats:
    #         tmp.append(cat)
    #     context['cats'] = tmp
    #     print(tmp)
    #     return render(request,'landing.html',context)