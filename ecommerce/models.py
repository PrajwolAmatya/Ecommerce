from django.db import models
from autoslug import AutoSlugField  # no need to add autoslug
from sorl.thumbnail import ImageField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import math


# Note: everything after . operator is member or attribute

class Category(models.Model):
    title = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='title', unique=True)
    image = ImageField()
    description = RichTextField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = RichTextField()
    price = models.DecimalField(max_digits=9999999999, decimal_places=2)
    brand = models.CharField(max_length=70)
    discount = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)  # remember one category can have many products(leader ko representation)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image(self):
        return self.producthasimage_set.first()  # selecting image(first) from list of image
        # self.producthasimage_set.first().image(): since we used product.image.image we don't use this

    def short_name(self):
        if len(self.title) > 45:
            return self.title[:42] + '...'
        return self.title

    def avg_rating(self):
        result = self.productreview_set.aggregate(models.Avg('rating'))  # check django aggregation doc
        if result['rating__avg'] == None:
            result['rating__avg'] = 0
        return math.ceil(result['rating__avg'])  # for ceiling purpose eg 4.95 lai 5 star


class ProductHasImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = ImageField()


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #
    rating = models.IntegerField()
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def total(self):
        return self.product.price * self.qty

    def __str__(self):
        return self.title
