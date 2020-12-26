from django.shortcuts import render
from django.http import JsonResponse

from .models import Store

def show_stores(request):
    if request.method == 'GET':
        stores = Store.objects.all()
        js_respond = {}
        for store in stores:
            js_respond[store.id] = str(store)
        return JsonResponse(js_respond)
    else:
        return JsonResponse({'status' : 'Bad Request !!!'})