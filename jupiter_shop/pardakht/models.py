from django.db import models
from ../user.models import user

class purchase(models.Model):

    orders = models.TextField('درخواست ها',max_length=100)
    user = models.ManyToManyField(user , on_delete = models.SET_DEFAULT , blank=True)

    def __str__(self):
        return self.user


    def reterive():
        pass



class payment(models.Model):

    payment_status = models.BooleanField(default=False)
    api_token = models.IntegerField(unique=True)

    def API():
        pass

class social(models.Model):

    jason_file = models.JSONField('متن')

    user = models.ForeignKey(user, on_delete=models.CASCADE)


    def use(request):

class order(models.Model):
    id = models.IntegerField(unique=True , blank= False)
