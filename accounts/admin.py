from django.contrib import admin
from .models import Account, Offer, Turno




# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('first_name','email','mobile','is_verified','date_joined','last_login' )
    readonly_fields = ('last_login','date_joined')
    filter_horizontal =()
    list_filter = ()
    fieldsets =()
    
    
admin.site.register(Account,AccountAdmin)



class OfferAdmin(admin.ModelAdmin):
    model = Offer
    list_display = ('name' , 'image')

class TurnoAdmin(admin.ModelAdmin):
    model = Turno
    list_display = ('name' , 'image')
admin.site.register(Offer, OfferAdmin)
admin.site.register(Turno, TurnoAdmin)