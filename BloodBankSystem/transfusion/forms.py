from django import forms
from django.forms import ModelForm

from accounts.models import Transfusion, Hospital


class TransfusionForm(ModelForm):
    hospital = forms.ModelChoiceField(widget=forms.Select(), queryset=Hospital.objects.only('user_id'))
    transfusion_date = forms.CharField(widget=forms.TextInput)
    status = False

    class Meta:
        model = Transfusion
        fields = ['hospital', 'transfusion_date']
