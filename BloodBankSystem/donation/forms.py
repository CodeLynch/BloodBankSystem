from django import forms
from django.forms import ModelForm

from accounts.models import Donation, BloodBank


class DonationForm(ModelForm):
    blood_bank = forms.ModelChoiceField(widget=forms.Select(), queryset=BloodBank.objects.only('user_id'))
    donation_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}), error_messages={'invalid': 'Please enter a valid date (yyyy-mm-dd).'})

    class Meta:
        model = Donation
        fields = ['blood_bank', 'donation_date']