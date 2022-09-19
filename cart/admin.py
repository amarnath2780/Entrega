from django.contrib import admin
from .models import AddressUser, Cart, CartEmpty , CartItem
# Register your models here.

class CartEmptyAdmin(admin.ModelAdmin):
    model = CartEmpty
    list_display = ('name' ,  'image')

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(AddressUser)
admin.site.register(CartEmpty , CartEmptyAdmin)