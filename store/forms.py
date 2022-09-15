from django import forms
from .models import ReviewRating

class ReviewForms(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject' , "review" , 'rating']