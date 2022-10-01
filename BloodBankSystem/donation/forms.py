from django import forms
from django.forms import ModelForm

from accounts.models import Donation, BloodBank


class DonationForm(ModelForm):
    bloodbank = forms.ModelChoiceField(widget=forms.Select(), queryset=BloodBank.objects.only('user_id'))
    donation_date = forms.CharField(widget=forms.TextInput)
    status = False

    class Meta:
        model = Donation
        fields = ['bloodbank', 'donation_date']