from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# ???????????
from address.models import Address
from user.models import User, Profile


def user_log(request, user_id):

    data = {}
    user_info = User.objects.filter(id=user_id)
    for obj in user_info:
        data = {'phonenumber': obj.phonenumber, 'user_type': obj.user_type, 'profile': {'name': obj.profile.ful_name, 'address': str(obj.profile.address)}}


    # user_info=User.objects.all().values()
    # data = {}
    # for obj in user_info:
    #     data[obj.get('id')] = obj
    #     for p_obj in Profile.objects.filter(id = obj.get('profile_id')).values():
    #         data[obj.get('id')].update({'Profile': p_obj})




    return JsonResponse(data, safe=False)
