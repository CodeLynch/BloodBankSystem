from django import forms
from accounts.models import *


cn_error_text = 'Please enter a valid contact number (09XXXXXXXXX).'
cn_placeholder = '09XXXXXXXXX'
age_max = 100
age_min = 0
weight_max = 100
weight_min = 0

class DonorForm(forms.ModelForm):
    type = 'I'
    individual_type = 'D'

    class Meta:
        model = Donor
        fields = ('user_image', 'username', 'password', 'first_name', 'middle_name', 'last_name', 'contact_number', 'age', 'weight', 'blood_type', 'health_condition')

        widgets = {
            'user_image': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'placeholder': cn_placeholder, 'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'max': weight_max, 'min': weight_min, 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'max': weight_max, 'min': weight_min, 'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'health_condition': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

        error_messages = {
            'contact_number': {
                'invalid': cn_error_text,
            },
        }

    def __init__(self, *args, **kwargs):
        super(DonorForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.individual_type = self.individual_type


class RecipientForm(forms.ModelForm):
    type = 'I'
    individual_type = 'R'

    class Meta:
        model = Recipient
        fields = ('user_image', 'username', 'password', 'first_name', 'middle_name', 'last_name', 'contact_number', 'age', 'weight', 'blood_type', 'health_condition')

        widgets = {
            'user_image': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'placeholder': cn_placeholder, 'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'max': weight_max, 'min': weight_min, 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'max': weight_max, 'min': weight_min, 'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'health_condition': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
        error_messages = {
            'contact_number': {
                'invalid': cn_error_text,
            },
        }

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.individual_type = self.individual_type


class HospitalForm(forms.ModelForm):
    type = 'O'
    org_type = 'H'

    class Meta:
        model = Hospital
        fields = ('user_image', 'username', 'password', 'name', 'address', 'contact_number')

        widgets = {
            'user_image': forms.FileInput(attrs={'class': 'form-control'}),
            'user_image': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'placeholder': cn_placeholder, 'class': 'form-control'}),
        }

        error_messages = {
            'contact_number': {
                'invalid': cn_error_text,
            },
        }

    def __init__(self, *args, **kwargs):
        super(HospitalForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.org_type = self.org_type


class BloodBankForm(forms.ModelForm):

    type = 'O'
    org_type = 'B'

    class Meta:
        model = BloodBank
        fields = ('user_image', 'username', 'password', 'name', 'address', 'contact_number')

        widgets = {
            'user_image': forms.FileInput(attrs={'class': 'form-control'}),
            'user_image': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'placeholder': cn_placeholder, 'class': 'form-control'}),
        }

        error_messages = {
            'contact_number': {
                'invalid': cn_error_text,
            },
        }

    def __init__(self, *args, **kwargs):
        super(BloodBankForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.org_type = self.org_type

