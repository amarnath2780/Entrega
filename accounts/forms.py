from django import forms

from cart.models import AddressUser
from .models import Account


class RegistrationForm(forms.ModelForm):
    
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
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'Email Address',
    }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': '10 digit Mobile',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Confirm Password',
    }))
    
    
    class Meta:

        model   = Account
        fields  = ['first_name','last_name','email','mobile','password','confirm_password']
        
    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password            = cleaned_data.get('password')
        confirm_password    = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('Password does not match')
        
        
        

class EditProfileForm(forms.ModelForm):
    
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
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'Lastname',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'email',
        'readonly': True,
    }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': '10 digit Mobile',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Confirm Password',
    }))
    class Meta:
    
        model   = Account
        fields  = ['first_name','last_name','mobile','email','password','confirm_password']
        
   




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










