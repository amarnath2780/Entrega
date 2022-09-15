from django.contrib import admin
from .models import Account




# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('first_name','email','mobile','is_verified','date_joined','last_login' )
    readonly_fields = ('last_login','date_joined')
    filter_horizontal =()
    list_filter = ()
    fieldsets =()
    
    
admin.site.register(Account,AccountAdmin)
