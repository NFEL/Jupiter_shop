from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

from .models import Category

@receiver(pre_save ,sender=Category)
def add_cat_checkeup(sender,instance,update_fields,raw,*args, **kwargs):

    if instance.id :
        print('Now You are updating nice')
    else:
        if 'shit' in instance.title.lower():
            instance.title = 'KhodeT , Bi Adab'
            # raise Exception('Baby be polite')
        if 'fuck' in instance.title.lower():
            # raw = False
            raise Exception('Bad Real Bad')
        if raw :
            print("you done commit true")
            