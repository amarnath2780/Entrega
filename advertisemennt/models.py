from pydoc import describe
from tokenize import Triple
from django.db import models

# Create your models here.
class Add(models.Model):
    name = models.CharField(max_length=200 , blank=True)
    image = models.ImageField(upload_to = 'images/add')
    decription = models.TextField(blank=True)


    def __str__(self):
        return self.name


class IconAdd(models.Model):
    name = models.CharField(max_length=200 , blank=True)
    image  = models.ImageField(upload_to = 'images/add')
    description = models.TextField(blank=True)


