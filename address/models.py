# from django.contrib.gis.db import models
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Address(models.Model):
    STATE = [
        ('tehran', 'تهران'),
        ('alborz', 'البرز'),
        ('markazi', 'مرکزی'),
    ]
    
    # location = models.PointField('موقعیت جغر0افیایی',geography=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    address_detail = models.TextField(blank=True,null=True)

    poste_code = models.CharField('کدپستی', max_length=50,blank=True, null=True)
    priority_address = models.SmallIntegerField(default=1)

    # objects = models.GeoManager()

    def __str__(self):
        return f'{self.user.username} -> {self.location}'
