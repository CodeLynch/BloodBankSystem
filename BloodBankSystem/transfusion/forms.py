from django import forms
from django.forms import ModelForm
from accounts.models import Transfusion, Hospital


class DateInput(forms.DateInput):
    input_type = 'date'
     

class TransfusionForm(ModelForm):
    # only include hospitals with blood supply in the choices
    hospital = forms.ModelChoiceField(widget=forms.Select(), queryset=Hospital.objects.only('user_id').exclude(blood_supply_id=None))
    transfusion_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Transfusion
        fields = ['hospital', 'transfusion_date']
