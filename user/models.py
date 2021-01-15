import os
import sys
import uuid
import threading,time,logging
from random import randrange
from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage


class User(AbstractUser):
    is_oauth = models.BooleanField(default=True)
    user_uuid = models.CharField(max_length=36, blank=True)
    phonenumber = models.CharField(max_length=12, blank=True,null=True,unique=True)

    user_join_date = models.DateField(auto_now_add=True)

    image = models.ImageField(
        upload_to='./res/profile_photo', blank=True, null=True)
    user_last_login = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['phonenumber','email'],name='only one email / phone per user'),
            ]

    def save(self, *args, **kwargs):
        
        if not self.id and not self.is_oauth :
            self.is_active = False

        return super().save(*args, **kwargs)



def reic(instance,*args, **kwargs):
    
    if not cache.get(instance.user_uuid) and not instance.is_active:
        
        if instance.email and isinstance(instance.email, str):
            instance.user_uuid = uuid.uuid4()
            try:
                start = time.time_ns()
                msg = EmailMessage(
                    'Signup via Email',
                    f'<a href="https://mapsa-jupiter-shop.herokuapp.com/user/verificationcode/{instance.user_uuid}">Verify me in the heroku</a>',
                    f'<a href="https://localhost:8000/user/verificationcode/{instance.user_uuid}">Verify me in the localhost</a>',
                    os.getenv('EMAIL_USERNAME'),
                    [instance.email, ])
                msg.content_subtype = "html"
                msg.send()
                end = time.time_ns()
                cache.set(instance.user_uuid, instance, timeout=60*2)
                instance.save()
                print('elapsed time to send email : ',(end-start)/1000000000)
                sys.stdout.flush()
            except Exception as e:
                print(type(e))
                instance.delete()
                
        if instance.phonenumber:
            instance.user_uuid = str(randrange(10000, 99999))

            # import kavenegar
            # api = kavenegar.KavenegarAPI('644D6F4C3675302F6571796658427877733553725474332F555A456A444F684A6A2F63313763665273696F3D')
            # params = { 'sender' : '1000596446', 'receptor': '09390084053', 'message' :f"Your Verification code is \n {instance.user_uuid}" }
            # response = api.sms_send( params)
            # print(response)

            import ghasedak
            sms = ghasedak.Ghasedak(
                "b9c691f59feea69cc4f28be37d0d2d655445a9098fdc702a1697d9fc499267dd")
            print(
                sms.send({'message': f"Your Verification code is \n {instance.user_uuid}",
                        'receptor': instance.phonenumber,  'linenumber': "10008566"})
            )
            cache.set(instance.user_uuid, instance, timeout=60*2)
            print(instance.user_uuid)
            instance.save()

        if not (instance.email and isinstance(instance.email, str) or instance.phonenumber):
            instance.delete()
        

post_save.connect(reic, weak=False, sender=User)
