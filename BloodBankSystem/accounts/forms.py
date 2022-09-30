from django.forms import ModelForm
from django import forms

from .models import *


class IndividualForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    type = 'I'
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    age = forms.IntegerField(widget=forms.NumberInput)
    weight = forms.FloatField(widget=forms.FloatField)
    contact_number = forms.CharField(widget=forms.TextInput)
    health_condition = models.CharField(widget=forms.Textarea)
    blood_type = models.CharField(widget=forms.ComboField)
    individual_type = models.CharField(widget=forms.ChoiceField)

    class Meta:
        model = Individual
        fields = ['username', 'password', 'first_name', 'last_name', 'age', 'weight', 'contact_number',
                  'health_condition', 'blood_type', 'individual_type']


class OrganizationForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    type = 'O'
    name = forms.CharField(widget=forms.TextInput)
    address = forms.CharField(widget=forms.TextInput)
    contact_number = forms.CharField(widget=forms.TextInput)
    org_type = forms.CharField(widget=forms.ChoiceField)

    class Meta:
        model = Organization
        fields = ['username', 'password', 'name', 'address', 'contact_number', 'weight', 'contact_number', 'org_type']


class BloodSupplyForm(ModelForm):
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


class DonationForm(ModelForm):
    donor = forms.CharField(widget=forms.ChoiceField)
    blood_bank = forms.CharField(widget=forms.ChoiceField)
    donation_date = models.DateField(widget=forms.DateField)
    status = False

    class Meta:
        model = Donation
        fields = ['donor', 'blood_bank', 'donation_date']


class TransfusionForm(ModelForm):
    recipient = models.CharField(widget=forms.ChoiceField)
    hospital = models.ForeignKey(widget=forms.ChoiceField)
    transfusion_date = models.DateField(widget=forms.DateField)
    status = False

    class Meta:
        model = Transfusion
        fields = ['recipient', 'hospital', 'transfusion_date']


class RequestForm(ModelForm):
    recipient = models.CharField(widget=forms.ChoiceField)
    hospital = models.ForeignKey(widget=forms.ChoiceField)
    transfusion_date = models.DateField(widget=forms.DateField)
    status = False

    class Meta:
        model = Transfusion
        fields = ['recipient', 'hospital', 'transfusion_date']
