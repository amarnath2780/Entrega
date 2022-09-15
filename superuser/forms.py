from django import forms
from order.models import Order, Payment
from store.models import Offers, Products
from django.utils.text import slugify



class Productform(forms.ModelForm):

    class Meta:
        model = Products
        fields = ['product_name' , 'product_name_card' , 'slug' , 'product_discription', 'product_discription1' , 'product_discription2' , 'product_highlights' , 'product_highlights1','product_highlights2' , 'product_highlights3', 'product_highlights4' ,'price' , 'pro_image1' , 'pro_image2' ,'pro_image3' , 'pro_image4' , 'pro_image5' , 'stock' , 'is_available' , 'category']

        
    def __init__(self,*args, **kwargs):
        super(Productform,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"]="form-control"


class Statusform(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status',] 
    

class Offerform(forms.ModelForm):

    class Meta:
        model = Offers
        fields = ['category', 'product' , 'offer']
