from pyexpat import model
from django import forms
from .models import *


max = 100
min = 0


class RequestBloodSupplyForm(forms.ModelForm):
    #only include blood banks with blood supply in the choices
    blood_bank = forms.ModelChoiceField(widget=forms.Select(), queryset=BloodBank.objects.only('user_id').exclude(blood_supply_id=None))
    blood_type = forms.CharField(widget=forms.Select()),
    request_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}), error_messages={'invalid': 'Please enter a valid date (yyyy-mm-dd).'})
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min}))

    class Meta:
        model = Request
        fields = ['blood_bank', 'blood_type', 'request_date', 'quantity']
