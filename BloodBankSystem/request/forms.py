from pyexpat import model
from django.forms import ModelForm
from django import forms
from .models import *


class RequestBloodSupplyForm(ModelForm):
    blood_type = forms.ChoiceField(widget=forms.Select())
    request_date = forms.DateField(widget=forms.DateInput)
    quantity = forms.IntegerField(widget=forms.NumberInput)

    class Meta:
        model = Request
        fields = ['blood_type', 'request_date', 'quantity']
