from django import forms
from .models import *


class BloodSupplyForm(forms.ModelForm):

    aplus_amount = forms.IntegerField(widget=forms.NumberInput),
    amin_amount = forms.IntegerField(widget=forms.NumberInput),
    bplus_amount = forms.IntegerField(widget=forms.NumberInput),
    bmin_amount = forms.IntegerField(widget=forms.NumberInput),
    abplus_amount = forms.IntegerField(widget=forms.NumberInput),
    abmin_amount = forms.IntegerField(widget=forms.NumberInput),
    oplus_amount = forms.IntegerField(widget=forms.NumberInput),
    omin_amount = forms.IntegerField(widget=forms.NumberInput),

    class Meta:
        model = BloodSupply
        fields = ['aplus_amount', 'amin_amount', 'bplus_amount', 'bmin_amount',
                  'abplus_amount', 'abmin_amount', 'oplus_amount', 'omin_amount']