from itertools import product
from tkinter import CASCADE
from django.db import models
from accounts.models import Account
from category.models import Category
from django.urls import reverse

# Create your models here.
class Products(models.Model):
    product_name = models.CharField(max_length=500 , unique=True)
    product_name_card = models.CharField(max_length=50 , unique=True)
    slug = models.SlugField(max_length=500 , unique=True)
    product_discription = models.TextField(blank=True)
    product_discription1 = models.TextField(blank=True)
    product_discription2 = models.TextField(blank=True)
    product_highlights = models.TextField(blank=True)
    product_highlights1 = models.TextField(blank=True)
    product_highlights2 = models.TextField(blank=True)
    product_highlights3 = models.TextField(blank=True)
    product_highlights4 = models.TextField(blank=True)
    price = models.IntegerField()
    pro_image1 = models.ImageField(upload_to = 'images/products ')
    pro_image2 = models.ImageField(upload_to = 'images/products ' , blank=True)
    pro_image3 = models.ImageField(upload_to = 'images/products ' , blank=True)
    pro_image4 = models.ImageField(upload_to = 'images/products ', blank=True)
    pro_image5 = models.ImageField(upload_to = 'images/products ' , blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    created_date =  models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_name  

    def get_url(self):
        return reverse('product_details' , args=[self.category.slug , self.slug])


variation_category_choice = {
    ('color' , 'color'),
    ('variant' , 'variant'),
}


class variation(models.Model):
    product = models.ForeignKey(Products , on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100 , choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Products , on_delete=models.CASCADE)
    user = models.ForeignKey(Account , on_delete=models.CASCADE)
    subject = models.CharField(max_length=1000 , blank=True)
    review = models.TextField(max_length=5000 , blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20 , blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.subject



class Offers(models.Model):
    category = models.OneToOneField(Category , on_delete=models.CASCADE)
    product = models.ForeignKey(Products , on_delete=models.CASCADE)
    offer = models.FloatField(blank=True)


    def __unicode__(self):
        return self.offer