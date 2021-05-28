from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint, Sum

from product.models import Product

User = get_user_model()

class Cart(models.Model):
    product = models.ManyToManyField(Product,through='CartItems')
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    
    # @property
    def my_price(self):
        cartitems = self.cartitems_set.select_related('product')
        sum_food_prices = 0
        for elm in cartitems:
            sum_food_prices += (elm.product.my_price() * elm.qty)
        return sum_food_prices
    
    def __str__(self):
        return str(self.user)

class CartItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    
    # @property
    def my_price(self):
        return self.product.my_price() * self.qty
    
    
    def __str__(self) -> str:
        return f'{self.product.name} -> {self.qty}'
    class Meta:
        constraints=[
            UniqueConstraint(
            name='unique_cartitems',
            fields=['cart','product'],)]
        
    

class Payment(models.Model):
    payment_status = models.BooleanField(default=False)
    api_token = models.IntegerField(unique=True)


class Social(models.Model):
    jason_file = models.JSONField('متن')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Purchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    # user = models.ManyToManyField(User)
    description = models.JSONField('ایتم های خریداری شده')
