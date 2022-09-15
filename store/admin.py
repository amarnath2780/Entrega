from django.contrib import admin
from .models import Offers, Products, variation , ReviewRating


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name' , 'price' , 'stock' ,'category' , 'pro_image1' , 'is_available') 
    prepopulated_fields = {'slug' : ('product_name',)}

class OfferAdmin(admin.ModelAdmin):
    list_display = ('category' , 'product' , 'offer')

admin.site.register(Products , ProductAdmin)
admin.site.register(variation)
admin.site.register(ReviewRating)
admin.site.register(Offers , OfferAdmin)
