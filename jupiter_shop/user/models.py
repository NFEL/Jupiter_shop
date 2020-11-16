from django.db import models
from address.models import Address

class user(models.Model):
    id=models
    phonenumber=models.IntegerField(null=False)
    passcode=models.CharField(max_length=64,null=False)
    User_Type=[("A",'user'),("B",'staff')]
    user_type=models.CharField(choices=User_Type,default="A")
    



class profile(models.Model):
    ful_name=models.CharField(max_length=40, null=False)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    postal_code=models.IntegerField()
    image=models.ImageField(upload_to='profile_photo')

    



