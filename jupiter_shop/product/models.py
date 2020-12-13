from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField('گروه', max_length=35, unique=True)
    description = models.JSONField('توضیحات گروه بندی', blank=True, null=True)
    image = models.ImageField(
        "عکس گروه", upload_to="category/", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Category'
        managed = True
        verbose_name = 'گروه بندی'
        verbose_name_plural = 'گروه بندی ها'


class SubCategory(models.Model):
    title = models.CharField('طبقه بندی', max_length=45)
    description = models.JSONField('توضیحات طبقه بندی', blank=True, null=True)
    its_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(
        "عکس طبقه بندی", upload_to="sub-category/")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Sub Category'
        managed = True
        verbose_name = 'طبقه بندی'
        verbose_name_plural = 'طبقه بندی ها'


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
    name = models.CharField('محصولات', max_length=100)
    # اگر محصول ناموجود باشد -> null
    stock_count = models.IntegerField('مقدار باقیمانده', default=0)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand, verbose_name=_(
        "Product Brand"), on_delete=models.CASCADE,blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    # ممکن است در بعضی موارد محصول گروه بندی نشود
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True,blank=True)
    description = models.JSONField(blank=True, null=True)


    image = models.ImageField(_("Product image"), upload_to='products/images/')




    user_responsible = models.ForeignKey(User, verbose_name=_("Responsible User"), on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f'{self.id} -> {self.name} [{self.stock_count} in stock]'

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
                              height_field=600, width_field=600, max_length=600)
    product = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ProductImage")
        verbose_name_plural = _("ProductImages")

    def __str__(self):
        return self.product.name

    # def get_absolute_url(self):
    #     return reverse("ProductImage_detail", kwargs={"pk": self.pk})
