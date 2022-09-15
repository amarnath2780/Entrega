import imp
from django.contrib import admin
from .models import Order , OrderProduct , Payment

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields =  [ 'user'  , 'quantity' , 'product_price'  ]
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display =  ['order_number' , 'full_name' , 'mobile' , 'email' , 'order_total' , 'tax' , 'status' , 'is_ordered']
    list_filter = ['status' , 'is_ordered']
    search_fields = ['order_number' , 'first_name' , 'last_name' , 'mobile' , 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order , OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)