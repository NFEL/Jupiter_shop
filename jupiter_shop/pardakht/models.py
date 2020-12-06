from django.db import models

from user.models import User
from product.models import Product


class Cart(models.Model):
    product = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.user)


class Payment(models.Model):
    payment_status = models.BooleanField(default=False)
    api_token = models.IntegerField(unique=True)


class Social(models.Model):
    jason_file = models.JSONField('متن')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Purchases(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # user = models.ManyToManyField(User)
    description = models.JSONField('ایتم های خریداری شده')
