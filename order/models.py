from itertools import product
from django.db import models
from accounts.models import Account
from store.models import Products, variation
# Create your models here.




class Payment(models.Model):
    user = models.ForeignKey(Account , on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    amount_paid = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('Ready for Shipping' , 'Ready for shipping'),
        ('Shipped' , 'Shipped'),
        ('Out for Delivery' , 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled' , 'Cancelled'),
    )

    user = models.ForeignKey(Account , on_delete=models.SET_NULL , null=True)
    payment =models.ForeignKey(Payment, on_delete=models.SET_NULL , blank=True , null=True)
    order_number = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200 , blank=True)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)
    order_note = models.CharField(max_length=300 , blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=30 , choices=STATUS , default='Ready for Shipping')
    ip = models.CharField(blank=True , max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    Payment = models.ForeignKey(Payment , on_delete=models.SET_NULL , blank=True , null=True)
    user = models.ForeignKey(Account , on_delete=models.CASCADE)
    product = models.ForeignKey(Products ,on_delete=models.CASCADE )
    varitations = models.ForeignKey(variation , on_delete=models.CASCADE  , blank=True , null=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.product_name