from audioop import add
from django.contrib import admin
from .models import Add , IconAdd

# Register your models here.


class AddAdmin(admin.ModelAdmin):
    model: Add
    list_display = ('name' , 'image')

class IconAddAdmin(admin.ModelAdmin):
    model: IconAdd
    list_display = ('name' , 'image')

admin.site.register(Add,AddAdmin)
admin.site.register(IconAdd , IconAddAdmin)