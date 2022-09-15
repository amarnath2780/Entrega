from django.contrib import admin
from .models import AddressUser, Cart , CartItem
# Register your models here.



admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(AddressUser)