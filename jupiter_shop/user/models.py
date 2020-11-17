from django.db import models
from address.models import Address


class User(models.Model):
    phonenumber = models.IntegerField(null=False)
    passcode = models.CharField(max_length=64, null=False)
    User_Type = [("A", 'user'), ("B", 'staff')]
    user_type = models.CharField(max_length=1, choices=User_Type, default="A")

    def __str__(self):
        return str(f'{self.id} - {self.phonenumber}')


class Profile(models.Model):
    ful_name = models.CharField(max_length=40, null=False)
    address = models.OneToOneField(
        Address, on_delete=models.SET_NULL, null=True)
    postal_code = models.IntegerField()
    image = models.ImageField(upload_to='./res/profile_photo')

    def __str__(self):
        return self.ful_name
