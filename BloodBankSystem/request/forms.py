from django import forms
from .models import *


max = 100
min = 0


# class DateInput(forms.DateInput):
#     input_type = 'date'


class RequestBloodSupplyForm(forms.ModelForm):
    #only include blood banks with blood supply in the choices
    blood_bank = forms.ModelChoiceField(label= 'Blood Bank',
        widget=forms.Select(attrs={'class': 'form-control'}), 
        queryset=BloodBank.objects.only('user_id').exclude(blood_supply_id=None))
    blood_type = forms.CharField(widget=forms.Select()),
    request_date = forms.DateField(widget=forms.DateInput(attrs={'type' : 'date', 'class':'form-control'}), label='Request Date')
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='Quantity')

    class Meta:
        model = Request
        fields = ['blood_bank', 'blood_type', 'request_date', 'quantity']

        widgets = {
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
        }
