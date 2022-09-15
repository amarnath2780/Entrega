from django.db import models
from accounts.models import Account
from store.models import Products, variation

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250 , blank=True)
    date = models.DateField(auto_now_add= True)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
   user = models.ForeignKey(Account , on_delete=models.CASCADE , null=True)
   variations = models.ManyToManyField(variation , blank=True)
   product = models.ForeignKey(Products , on_delete=models.CASCADE) 
   cart = models.ForeignKey(Cart , on_delete=models.CASCADE , null=True)
   quantity = models.IntegerField()
   is_active = models.BooleanField(default=True)

   def sub_total(self):
    return self.product.price * self.quantity


   def __unicode__(self):
        return self.product

ADD_TYPE = (
    ("Home", "Home"),
    ("Word", "Work"),
)


class AddressUser(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    add_type = models.CharField(max_length=50 , choices=ADD_TYPE)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
    def full_address(self):
        return f"{self.address1}, {self.address2}"

    