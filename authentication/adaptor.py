from allauth.account.utils import user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMakerAdaptor(DefaultSocialAccountAdapter):

    def new_user(self, request, sociallogin):
        return User(
            username=sociallogin.email_addresses, email=sociallogin.email_addresses)
        

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = data.get('first_name') + "_" + \
            data.get('last_name' or '')
        i = 0
        while User.objects.filter(username = user.username).exists():
            user.username = data.get('first_name') + \
                "_" + data.get('last_name' or '') + str(i)
            i += 1
        return user

    def save_user(self, request, sociallogin, form=None):
        self.is_active = True
        return super().save_user(request=request, sociallogin=sociallogin, form=None)
