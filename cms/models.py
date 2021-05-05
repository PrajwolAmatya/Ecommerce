from django.db import models
from sorl.thumbnail import ImageField
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField  # no need to add autoslug


class Banner(models.Model):
    caption = models.CharField(max_length=70)
    image = ImageField()
    weight = models.IntegerField()
    published = models.BooleanField()

    def __str__(self):
        return str(self.weight)


class Page(models.Model):  # always singular name for model
    title = models.CharField(max_length=70)
    menu_title = models.CharField(max_length=70)
    content = RichTextField()
    image = ImageField()
    published = models.BooleanField()
    navbar = models.BooleanField()  # hamro page ma navbar aaune ki naaune
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=20)
    image = ImageField()
