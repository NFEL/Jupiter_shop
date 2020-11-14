from django.db import models

from user.models import Profile
from product.models import Category, SubCategory
from address.models import Address


class Store(models.Model):
    categories = models.models.ManyToManyField(Category, verbose_name=_("Categories of Store"))
    sub_categories = models.models.ManyToManyField(SubCategory, verbose_name=_("Sub Categories of Store"))
    address = models.ForeignKey('آدرس',Address,on_delete=models.CASCADE)
    store_name = models.CharField('نام نمایشی',max_length=30)
    is_verified = models.BooleanField('رسمی',default=False)

    class class Meta:
        db_table = 'Store'
        managed = True
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return self.store_name