import re,threading
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
        user_id = request.session.get('user_obj', None)
        if user_id:
            user_obj = User.objects.get(id=user_id)
            if not user_obj.is_active and not cache.get(user_obj.user_uuid):
                # user = User.objects.get(id=request.session['user_obj'])
                cache.delete(user_obj.user_uuid)
                request.session['user_obj'] = None
                user_obj.delete()
                return redirect('user-login')

        return render(request, self.template, self.context)

    def post(self, request, *args, **kwargs):
        try:
            is_signin = request.POST.get('signin')
            is_signup = request.POST.get('signup')
            is_forgotpass = request.POST.get('forgot-password-form')
            given_uuid = request.POST.get('signup-uuid-given')
            delete_user = request.POST.get('signup-delete-user')
            user_obj = request.session.get('user_obj', None)

            if is_forgotpass:
                email_phone = request.POST.get(
                    'signin-forgot-password-email-phone')
                new_pass = request.POST.get('signin-forgot-password-new')
                regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
                regex_phone = '^[a-z0-9]+'

                is_phone = re.search(regex_phone, email_phone)
                is_email = re.search(regex_email, email_phone)

                type = ''
                message = ''
                if is_phone:
                    type = 'phone'
                else:
                    message = 'Phone is not registered in system \n'
                if is_email:
                    type = 'email'
                else:
                    message = 'Email is not registered in system \n'
                if not is_email and not is_phone:
                    message = 'Niether one signed before'

                messages.add_message(request, messages.ERROR, message)

                self.reset_pass(new_pass, email_phone, type=type)

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
                    for user in User.objects.all():
                        if name == user.username:
                            messages.add_message(request, messages.ERROR,
                                                 'User exists ... ')
                            return redirect('user-login')

                    if email and phone_number:
                        user_obj = User.objects.create_user(
                            username=name, email=email, phonenumber=phone_number, password=password)
                    elif not email and phone_number:
                        user_obj = User.objects.create_user(
                            username=name, phonenumber=phone_number, password=password)
                    elif email and not phone_number:
                        user_obj = User.objects.create_user(
                            username=name, email=email, password=password)
                    if not email and not phone_number:
                        messages.add_message(request, messages.ERROR,
                                             'SomeThing to get to know you my friend ...')
                        return redirect('user-login')

                    if user_obj:
                        request.session['user_obj'] = user_obj.id
                        if not user_obj.phonenumber:
                            messages.add_message(request, messages.ERROR,
                                                 'Check Your inbox ...')
                        else:
                            messages.add_message(request, messages.ERROR,
                                                 'Enter the key generated for you...')

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

    def reset_pass(self, new_pass, email_phone, type):
        if not type:
            return False
        elif type == 'phone':
            # def validatePhone_reset_pass():
                
            #     import ghasedak
            #     sms = ghasedak.Ghasedak(
            #         "b9c691f59feea69cc4f28be37d0d2d655445a9098fdc702a1697d9fc499267dd")
            #     print(
            #         sms.send({'message': f"Your Verification code is \n {instance.user_uuid}",
            #                 'receptor': instance.phonenumber,  'linenumber': "10008566"})
            #     )
            
            # reset_pass_thread = threading.Thread(target=validatePhone_reset_pass).start()
            
            user = User.objects.get(phonenumber=email_phone)
            user.set_password(new_pass)
            user.save()
            print('done')
            return True
        elif type == 'email':
            user = User.objects.get(email=email_phone)
            user.set_password(new_pass)
            user.save()

            return True
        return False




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
