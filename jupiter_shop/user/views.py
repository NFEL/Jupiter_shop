from django.contrib import auth
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth import login,logout,user_logged_in,authenticate
from django.contrib.auth.models import Permission,Group,User
# ???????????
# from address.models import Address
from .models import Profile


def logggin(sender,request,user,*args, **kwargs):
    # print(type(sender))
    # print(args)
    # print(kwargs)
    # print(request)
    # print(request.user)
    # print(f'And welcome from view, dear{ user }')
    print(f'Welcome to {user} from {__name__}')
    pass

    

user_logged_in.connect(logggin)

def user_log(request, user_id):

    data = {}
    user_info = User.objects.filter(id=user_id)
    for obj in user_info:
        data = {'phonenumber': obj.phonenumber, 'user_type': obj.user_type, 'profile': {
            'name': obj.profile.ful_name, 'address': str(obj.profile.address)}}

    # user_info=User.objects.all().values()
    # data = {}
    # for obj in user_info:
    #     data[obj.get('id')] = obj
    #     for p_obj in Profile.objects.filter(id = obj.get('profile_id')).values():
    #         data[obj.get('id')].update({'Profile': p_obj})


    return JsonResponse(data, safe=False)

class UserVerification(View):
    template = 'profile/profile_detail.html'
    context = {}
    def get(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            self.context['username'] = request.user

            return render(request,self.template,self.context)
            # return redirect('user-profile')
        else:
            return render(request,self.template,self.context)
    
    def post(self,request,*args, **kwargs):
        try:
            is_signin = request.POST.get('signin')
            is_signup = request.POST.get('signup')

            if is_signup:
                phone_number = request.POST.get('signup-phone_number')
                name = request.POST.get('signup-username')
                password = request.POST.get('signup-password')
                if password :
                    profile_obj = Profile.objects.create(ful_name=name,phonenumber=phone_number,password=password)
                else:
                    profile_obj = Profile.objects.create(ful_name=name,phonenumber=phone_number)
                
                profile_obj.save()
                login(profile_obj.user_id)
                return redirect('categories')
            if is_signin:
                username = request.POST.get('signin-username')    
                password = request.POST.get('signin-password')   
                
                user_obj = login(request,
                                 user = authenticate(request,username,password))
                return redirect('categories')
        except Exception as e:
            print(e)

class UserProfile(View):
    pass