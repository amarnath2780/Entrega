from django import forms

from cart.models import AddressUser

class AddressForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput ',
        'placeholder': 'Firstname',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'Lastname',

    }))
    building = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput ',
        'placeholder': 'building',
    }))
    street = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'street',

    }))
    district = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput ',
        'placeholder': 'district',
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'state',

    }))
    pin_code = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'type': 'number',
        'placeholder': 'pin',

    }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput ',
        'type': 'number',
        'placeholder': 'mobile',
    }))
    alt_mobile = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'type': 'number',
        'placeholder': 'alternate mobile',

    }))
    
    class Meta:
        model  = AddressUser
        fields = ['first_name','last_name','building','street','district','pin_code','state','mobile','alt_mobile'] 



class AddAdddressForm(forms.ModelForm):
    class Meta:
        model = AddressUser
        fields = (
            "first_name",
            "last_name",
            "phone",
            "email",
            "address1",
            "address2",
            "country",
            "state",
            "city",
            "pincode",
            "add_type",
        )

    def __init__(self,*args,**kwargs):
        super(AddAdddressForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"]="form-control"