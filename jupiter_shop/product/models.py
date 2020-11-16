from django.db import models


class Category(models.Model):
    title = models.CharField('گروه',max_length=35)
    description = models.JSONField('توضیحات گروه بندی')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Category'
        managed = True
        verbose_name = 'گروه بندی'
        verbose_name_plural = 'گروه بندی ها'

class SubCategory(models.Model):
    title = models.CharField('طبقه بندی' , max_length=45)
    description = models.JSONField('توضیحات طبقه بندی')

    def __str__(self):
        return self.title

        
    class Meta:
        db_table = 'Sub Category'
        managed = True
        verbose_name = 'ظبقه بندی'
        verbose_name_plural = 'ظبقه بندی ها'



from store.models import Store



class Product(models.Model):
    name = models.CharField('محصولات', max_length=100)
    price = models.FloatField('قیمت محصول',null=True) ## اگر محصول ناموجود باشد -> null
    stock_count = models.IntegerField('مقدار باقیمانده',default= 0)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)    
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL,null=True) ## ممکن است در بعضی موارد محصول گروه بندی نشود
    description = models.JSONField()


    def __str__(self):
        return f'{self.id} -> {self.name} [{self.stock_count} in stock]'
    
    class Meta:
        db_table = 'Products'
