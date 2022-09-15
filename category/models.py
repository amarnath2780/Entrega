from distutils.command.upload import upload
from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=300 , unique=True)
    slug = models.SlugField(max_length=300 , unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField( upload_to = 'images/category' , blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def get_url(self):
        return reverse('products_by_category' ,args=[self.slug])

    def __str__(self):
        return self.category_name




