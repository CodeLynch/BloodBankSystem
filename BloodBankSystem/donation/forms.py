from datetime import date, datetime
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from accounts.models import Donation, BloodBank


class DateInput(forms.DateInput):
    input_type = 'date'
    

class DonationForm(ModelForm):

    #choices only include blood banks with blood supply

    blood_bank = forms.ModelChoiceField(label='Blood Bank',
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        queryset=BloodBank.objects.only('user_id').exclude(blood_supply_id=None))
    donation_date = forms.DateField(label='Donation Date',widget=DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Donation
        fields = ['blood_bank', 'donation_date']

    def clean_donation_date(self):
        don_date = datetime.strptime(self.data.get('donation_date'), '%Y-%m-%d').date()
        if don_date < date.today():
            raise ValidationError('Date must be today or later!')
        else:
            return don_date
