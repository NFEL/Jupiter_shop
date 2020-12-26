import os
import uuid
from random import randrange
from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage


class User(AbstractUser):
    user_uuid = models.CharField(max_length=36, blank=True)
    phonenumber = models.CharField(max_length=12, null=False)

    user_join_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.is_active = False
        return super().save(*args, **kwargs)


def reic(sender, instance, *args, **kwargs):

    if not cache.get(instance.user_uuid) and not instance.is_active:
        if instance.email and isinstance(instance.email, str):
            instance.user_uuid = uuid.uuid4()
            msg = EmailMessage(
                'Signup via Email',
                f'<a href="http://127.0.0.1:8000/user/verificationcode/{instance.user_uuid}">Verify me</a>',
                os.getenv('EMAIL_USERNAME'),
                [instance.email, ])
            msg.content_subtype = "html"
            msg.send()
            cache.set(instance.user_uuid, instance, timeout=60*2)
            instance.save()

        if instance.phonenumber:
            instance.user_uuid = str(randrange(10000, 99999))
            cache.set(instance.user_uuid, instance, timeout=60*2)
            instance.save()
            # send_verification()
        if not (instance.email and isinstance(instance.email, str) or instance.phonenumber):
            instance.delete()
        print(instance.user_uuid)


post_save.connect(reic, weak=False, sender=User)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.RESTRICT, primary_key=True, blank=True)
    address = models.OneToOneField(
        'address.Address', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(
        upload_to='./res/profile_photo', blank=True, null=True)
    user_last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.ful_name:
            return f'{self.ful_name} - {self.phonenumber}'
        else:
            return str(self.id)
