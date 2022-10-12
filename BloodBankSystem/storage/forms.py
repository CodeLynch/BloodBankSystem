from django import forms
from .models import *


max = 100
min = 0


class BloodSupplyForm(forms.ModelForm):

    aplus_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='A+ amount')
    amin_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='A- amount')
    bplus_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='B+ amount')
    bmin_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='B- amount')
    abplus_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='AB+ amount')
    abmin_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='AB- amount')
    oplus_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='O+ amount')
    omin_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'max': max, 'min': min, 'class': 'form-control'}), label='O- amount')

    class Meta:
        model = BloodSupply
        fields = ['aplus_amount', 'amin_amount', 'bplus_amount', 'bmin_amount',
                  'abplus_amount', 'abmin_amount', 'oplus_amount', 'omin_amount']