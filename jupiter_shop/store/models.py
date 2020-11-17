from django.db import models

from user.models import Profile
from product.models import Category, SubCategory
from address.models import Address


class Store(models.Model):
    categories = models.ManyToManyField(Category, verbose_name="Categories inside Store")
    sub_categories = models.ManyToManyField(SubCategory, verbose_name="Sub Categories inside Store")
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    store_name = models.CharField('نام نمایشی',max_length=30)
    is_verified = models.BooleanField('رسمی',default=False)

    class Meta:
        db_table = 'Store'
        managed = True
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return self.store_name