from django import forms
from django.forms import ModelForm
from accounts.models import Donation, BloodBank


class DateInput(forms.DateInput):
    input_type = 'date'
    

class DonationForm(ModelForm):
    #choices only include blood banks with blood supply
    blood_bank = forms.ModelChoiceField(widget=forms.Select(), queryset=BloodBank.objects.only('user_id').exclude(blood_supply_id=None))
    donation_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Donation
        fields = ['blood_bank', 'donation_date']