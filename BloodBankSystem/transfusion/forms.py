from django import forms
from django.forms import ModelForm
from accounts.models import Transfusion, Hospital


class DateInput(forms.DateInput):
    input_type = 'date'
     

class TransfusionForm(ModelForm):
    # only include hospitals with blood supply in the choices
    hospital = forms.ModelChoiceField(label='Hospital',
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Hospital.objects.only('user_id').exclude(blood_supply_id=None))
    transfusion_date = forms.DateField(label='Transfusion Date',widget=DateInput(attrs={'class': 'form-control'}))
    requested_blood_type = forms.ChoiceField(label='Blood Type',widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Transfusion
        fields = ['hospital', 'transfusion_date', 'requested_blood_type']

    def __init__(self, blood_type, *args, **kwargs):
        super(TransfusionForm, self).__init__(*args, **kwargs)
        choices = ()
        if blood_type == 'A+':
            choices = (('A+', 'A+'), ('A-', 'A-'), ('O+', 'O+'), ('O-', 'O-'))
        elif blood_type == 'O+':
            choices = (('O+', 'O+'), ('O-', 'O-'))
        elif blood_type == 'B+':
            choices = (('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'))
        elif blood_type == 'AB+':
            choices = (('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-'))
        elif blood_type == 'A-':
            choices = (('A-', 'A-'), ('O-', 'O-'))
        elif blood_type == 'O-':
            choices = (('O-', 'O-'),)
        elif blood_type == 'B-':
            choices = (('B-', 'B-'), ('O-', 'O-'))
        elif blood_type == 'AB-':
            choices = (('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-'))
        self.fields['requested_blood_type'].choices = choices
