from pyexpat import model
from django import forms
from .models import *


class RequestBloodSupplyForm(forms.ModelForm):
    blood_type = forms.CharField(widget=forms.Select()),
    request_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}), error_messages={'invalid': 'Please enter a valid date (yyyy-mm-dd).'})
    quantity = forms.IntegerField(widget=forms.NumberInput()),

    class Meta:
        model = Request
        fields = ['blood_type', 'request_date', 'quantity']
