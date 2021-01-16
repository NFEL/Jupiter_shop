import abc
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

from store.models import Store
User = get_user_model()


class AddressAbstract(models.Model):

    location = models.PointField('موقعیت جغرافیایی', geography=True)
    address_detail = models.TextField(blank=True, null=True)

    poste_code = models.CharField(
        'کدپستی', max_length=50, blank=True, null=True)
    priority_address = models.SmallIntegerField(default=1)

    class Meta:
        abstract = True
        ordering = ('priority_address', 'location', )


class UserAdress(AddressAbstract):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} -> {self.location}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_priority_user_location',
                fields=['user', 'priority_address'],)]
        


class StoreAddress(AddressAbstract):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    working_raduis = models.IntegerField(default=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_priority_user_location',
                fields=['store', 'priority_address'],)]
