from django import forms
from django.forms import ModelForm

from accounts.models import Transfusion, Hospital


class TransfusionForm(ModelForm):
    # only include hospitals with blood supply in the choices
    hospital = forms.ModelChoiceField(widget=forms.Select(), queryset=Hospital.objects.only('user_id').exclude(blood_supply_id=None))
    transfusion_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}), error_messages={'invalid': 'Please enter a valid date (yyyy-mm-dd).'})

    class Meta:
        model = Transfusion
        fields = ['hospital', 'transfusion_date']
