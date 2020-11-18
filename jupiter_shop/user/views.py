from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#???????????
from address.models import Address
from user.models import User,Profile


def user_log(request,user_id):
    
    user_info=User.objects.filter(id=user_id).values()

    data = {'phonenumber':user_info.phonenumber, 'user_type':user_info.user_type}
    print(user_info)
    print("hello")
    return JsonResponse(data, safe=False)



    

