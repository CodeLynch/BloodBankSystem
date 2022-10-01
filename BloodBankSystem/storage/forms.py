from django.forms import ModelForm
from django import forms
from .models import *


class CreateBloodSupplyForm(ModelForm):

    aplus_amount = forms.IntegerField(widget=forms.NumberInput)
    amin_amount = forms.IntegerField(widget=forms.NumberInput)
    bplus_amount = forms.IntegerField(widget=forms.NumberInput)
    bmin_amount = forms.IntegerField(widget=forms.NumberInput)
    abplus_amount = forms.IntegerField(widget=forms.NumberInput)
    abmin_amount = forms.IntegerField(widget=forms.NumberInput)
    oplus_amount = forms.IntegerField(widget=forms.NumberInput)
    omin_amount = forms.IntegerField(widget=forms.NumberInput)

    class Meta:
        model = BloodSupply
        fields = ['aplus_amount', 'amin_amount', 'bplus_amount', 'bmin_amount',
                  'abplus_amount', 'abmin_amount', 'oplus_amount', 'omin_amount']

    def __init__(self, *args, **kwargs):
        super(CreateBloodSupplyForm, self).__init__(*args, **kwargs)
        self.fields['aplus_amount'].label = "A+ amount"
        self.fields['amin_amount'].label = "A- amount"
        self.fields['bplus_amount'].label = "B+ amount"
        self.fields['bmin_amount'].label = "B- amount"
        self.fields['abplus_amount'].label = "AB+ amount"
        self.fields['abmin_amount'].label = "AB- amount"
        self.fields['oplus_amount'].label = "O+ amount"
        self.fields['omin_amount'].label = "O- amount"


class UpdateBloodSupplyForm(ModelForm):
    aplus_amount = forms.IntegerField(widget=forms.NumberInput)
    amin_amount = forms.IntegerField(widget=forms.NumberInput)
    bplus_amount = forms.IntegerField(widget=forms.NumberInput)
    bmin_amount = forms.IntegerField(widget=forms.NumberInput)
    abplus_amount = forms.IntegerField(widget=forms.NumberInput)
    abmin_amount = forms.IntegerField(widget=forms.NumberInput)
    oplus_amount = forms.IntegerField(widget=forms.NumberInput)
    omin_amount = forms.IntegerField(widget=forms.NumberInput)

    class Meta:
        model = BloodSupply
        fields = ['aplus_amount', 'amin_amount', 'bplus_amount', 'bmin_amount',
                  'abplus_amount', 'abmin_amount', 'oplus_amount', 'omin_amount']

    def __init__(self, *args, **kwargs):
        super(UpdateBloodSupplyForm, self).__init__(*args, **kwargs)
        self.fields['aplus_amount'].label = "A+ amount"
        self.fields['amin_amount'].label = "A- amount"
        self.fields['bplus_amount'].label = "B+ amount"
        self.fields['bmin_amount'].label = "B- amount"
        self.fields['abplus_amount'].label = "AB+ amount"
        self.fields['abmin_amount'].label = "AB- amount"
        self.fields['oplus_amount'].label = "O+ amount"
        self.fields['omin_amount'].label = "O- amount"