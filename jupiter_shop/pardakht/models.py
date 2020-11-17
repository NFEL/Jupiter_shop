from django.db import models

from user.models import User
from product.models import Product


class Cart(models.Model):
    product = models.ManyToManyField(Product)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.user


class Payment(models.Model):
    payment_status = models.BooleanField(default=False)
    api_token = models.IntegerField(unique=True)


class Social(models.Model):
    jason_file = models.JSONField('متن')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Purchases(models.Model):
    user = models.ManyToManyField(User)
    description = models.JSONField('ایتم های خریداری شده')
