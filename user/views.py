from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.cache import cache
from django.db.utils import IntegrityError

User = auth.get_user_model()


class UserVerification(View):
    template = 'profile/profile_detail.html'
    context = {}

    def get(self, request, *args, **kwargs):

        return render(request, self.template, self.context)

    def post(self, request, *args, **kwargs):
        try:
            is_signin = request.POST.get('signin')
            is_signup = request.POST.get('signup')
            given_uuid = request.POST.get('signup-uuid-given')
            delete_user = request.POST.get('signup-delete-user')

            if delete_user:
                user = User.objects.get(id=request.session['user_obj'])
                cache.delete(user.user_uuid)
                request.session['user_obj'] = None
                user.delete()
                return redirect('user-login')

            if given_uuid:
                return redirect('verification', user_uuid=given_uuid)

            if is_signup:
                phone_number = request.POST.get('signup-phone_number')
                password = request.POST.get('signup-password')
                name = request.POST.get('signup-username')
                email = request.POST.get('signup-email')

                try:
                    profile_obj = None

                    for user in User.objects.all():
                        if name == user.username:
                            messages.add_message(request, messages.ERROR,
                                                 'User exists ... ')
                            return redirect('user-login')

                    if email and phone_number:
                        profile_obj = User.objects.create(
                            username=name, email=email, phonenumber=phone_number)
                    elif not email and phone_number:
                        profile_obj = User.objects.create(
                            username=name, phonenumber=phone_number)
                    elif email and not phone_number:
                        profile_obj = User.objects.create(
                            username=name, email=email)
                    if not email and not phone_number:
                        messages.add_message(request, messages.ERROR,
                                             'SomeThing to get to know you Friend ...')
                        return redirect('user-login')

                    if profile_obj:
                        profile_obj.set_password(password)
                        request.session['user_obj'] = profile_obj.id
                    return redirect('user-login')
                except IntegrityError as e:
                    print(e)
                    messages.add_message(request, messages.ERROR,
                                         'User exists with this Email/Phone')
                    return redirect('user-login')
                except Exception as e:
                    print(e)
                    messages.add_message(request, messages.ERROR,
                                         'Crash As Always, try again ...')
                    return redirect('user-login')

            if is_signin:
                username = request.POST.get('signin-username')
                password = request.POST.get('signin-password')
                user = authenticate(
                    request, username=username, password=password)
                if user:
                    login(request, user=user)
                    return redirect('categories')
                else:
                    messages.add_message(request, messages.INFO,
                                         'Bad Credential, Try Again ...')
                    return redirect('user-login')
            if not is_signin and not is_signup:
                messages.add_message(request, messages.INFO,
                                     'Bad Requset, X_X')
                return redirect('user-login')
        except Exception as e:
            print(e)
            return redirect('user-login')


class UserProfile(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('OK')
        else:
            return redirect('user-login')


def logout_user(request, *args, **kwargs):
    if request.user.is_authenticated:
        logout(request)
    return redirect('user-login')


def receive_user_uuid(request, user_uuid, *args, **kwargs):

    if user_uuid:
        try:

            user = cache.get(user_uuid)
            if user:
                if user.is_active:
                    messages.add_message(request, messages.INFO,
                                         'Already Verified')
                else:
                    try:
                        user.is_active = True
                        user.save()
                        cache.delete(user_uuid)
                        request.session['user_obj'] = None
                        messages.add_message(request, messages.INFO,
                                             'Success :)')
                        login(request, user)
                    except Exception as e:
                        print(e)
            else:
                messages.add_message(request, messages.INFO,
                                     'Bad Code')
            return redirect('user-login')

        except Exception as e:
            print(e)
            return HttpResponse('Unhandled Error')
