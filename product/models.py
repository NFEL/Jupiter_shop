from django.db import models
from django.db.models.query_utils import select_related_descend
from django.dispatch import receiver
from django.core.cache import cache,utils
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.db.models import UniqueConstraint, Avg,signals
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

class Category(models.Model):
    title = models.CharField('گروه', max_length=35, unique=True)
    description = models.TextField('توضیحات گروه بندی', blank=True, null=True)
    image = models.ImageField(
        "عکس گروه", upload_to="category/", blank=True, null=True)

    def __str__(self):
        return self.title

    
    def my_brands(self):
        return ProductBrand.objects.filter(brands__category = self)
    
    @classmethod
    def my_brands(cls,title):
        return ProductBrand.objects.filter(brands__category__title = title)

    class Meta:
        db_table = 'Category'
        managed = True
        verbose_name = 'گروه بندی'
        verbose_name_plural = 'گروه بندی ها'


class SubCategory(models.Model):
    title = models.CharField('طبقه بندی', max_length=45)
    description = models.TextField('توضیحات طبقه بندی', blank=True, null=True)
    its_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(
        "عکس طبقه بندی", upload_to="sub-category/")

    def __str__(self):
        return self.title

    def my_brands(self):
        return ProductBrand.objects.filter(brands__sub_category = self)
    
    @classmethod
    def my_brands(cls,title):
        return ProductBrand.objects.filter(brands__sub_category__title = title)

    class Meta:
        db_table = 'Sub Category'
        managed = True
        verbose_name = 'طبقه بندی'
        verbose_name_plural = 'طبقه بندی ها'
        constraints=[
            UniqueConstraint(
            name='unique_order',
            fields=['title','its_category'],)]


class ProductBrand(models.Model):

    name = models.CharField(_("Brand name"), max_length=50)
    image = models.ImageField(_("Brand image"), upload_to="products/brands/",
                              blank=True, null=True)

    class Meta:
        verbose_name = _("productbrand")
        verbose_name_plural = _("productbrands")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('نام محصول', max_length=100)
    # اگر محصول ناموجود باشد -> null
    stock_count = models.IntegerField('مقدار باقیمانده', default=0)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand, verbose_name=_(
        "Product Brand"), on_delete=models.CASCADE,blank=True, null=True,related_name='brands')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    # ممکن است در بعضی موارد محصول گروه بندی نشود
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True,blank=True)
    description = models.JSONField(blank=True, null=True)

    
    image = models.ImageField(_("thumbtnail"), upload_to='products/images/')
    user_responsible = models.ForeignKey(User, verbose_name=_("Responsible User"), on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f'{self.id} -> {self.name} [{self.stock_count} in stock]'

    def my_rate(self):
        return self.productcomment_set.all().aggregate(Avg('rate')).get('rate__avg',None)
    
    def my_price(self):
        if self.productprice_set.all():
            return self.productprice_set.all().order_by('-datetime__minute')[0].price
        else:
            return 0
    def my_images(self):
        return self.productimage_set.all()
    def my_comments(self):
        return self.productcomment_set.all()
    class Meta:
        db_table = 'Products'


class ProductPrice(models.Model):

    date = models.DateField(_("date of this price"), auto_now_add=True)
    datetime = models.DateTimeField(_("datetime"), auto_now_add=True)
    product = models.ForeignKey(Product, verbose_name=_(
        "Product"), on_delete=models.CASCADE)
    price = models.FloatField(_("Price"))

    class Meta:
        verbose_name = _("productprice")
        verbose_name_plural = _("productprices")

    def __str__(self):
        return f'{self.id} -> {self.price} ({self.date}) - ({self.datetime})'


class ProductImage(models.Model):

    image = models.ImageField("عکس محصول", upload_to="products/",
                              )
    name = models.CharField(_("image_name"), max_length=50)
    product = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ProductImage")
        verbose_name_plural = _("ProductImages")

    def __str__(self):
        return self.product.name

    # def get_absolute_url(self):
    #     return reverse("ProductImage_detail", kwargs={"pk": self.pk})

class ProductComment(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(""), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    rate = models.FloatField(_(""),validators=[MinValueValidator(0), MaxValueValidator(5)],)
    text = models.CharField(_(""), max_length=350)


##cahce for diffrent parts of page
# @receiver(signals.post_save,sender=Product)
# @receiver(signals.post_save,sender=Category)
# @receiver(signals.post_save,sender=SubCategory)
# @receiver(signals.post_save,sender=SubCategory)
# @receiver(signals.post_save,sender=SubCategory)
# @receiver(signals.post_save,sender=SubCategory)
# @receiver(signals.post_save)
def update_product_view(sender, instance, **kwargs):
    """
    docstring
    """
    print('hey')
    key = utils.make_template_fragment_key('landing-whole-page')
    try:
        cache.delete(key)
    except Exception as e:
        raise ValueError(e)
    