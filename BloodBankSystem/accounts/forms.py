from django import forms
from accounts.models import *


class DonorForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    type = 'I'
    first_name = forms.CharField(widget=forms.TextInput())
    middle_name = forms.CharField(widget=forms.TextInput()),
    last_name = forms.CharField(widget=forms.TextInput())
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '09XXXXXXXXX'}), error_messages={'invalid': 'Please enter a valid contact number (09XXXXXXXXX).'})
    age = forms.IntegerField(widget=forms.NumberInput())
    weight = forms.FloatField(widget=forms.NumberInput()),
    blood_type = forms.CharField(widget=forms.Select()),
    health_condition = forms.CharField(widget=forms.Textarea()),
    individual_type = 'D'

    class Meta:
        model = Donor
        fields = ('username', 'password', 'first_name', 'middle_name', 'last_name', 'contact_number', 'age', 'weight', 'blood_type', 'health_condition')

    def __init__(self, *args, **kwargs):
        super(DonorForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.individual_type = self.individual_type


class RecipientForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    type = 'I'
    first_name = forms.CharField(widget=forms.TextInput())
    middle_name = forms.CharField(widget=forms.TextInput()),
    last_name = forms.CharField(widget=forms.TextInput())
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '09XXXXXXXXX'}), error_messages={'invalid': 'Please enter a valid contact number (09XXXXXXXXX).'})
    age = forms.IntegerField(widget=forms.NumberInput())
    weight = forms.FloatField(widget=forms.NumberInput()),
    blood_type = forms.CharField(widget=forms.Select()),
    health_condition = forms.CharField(widget=forms.Textarea()),
    individual_type = 'R'

    class Meta:
        model = Recipient
        fields = ('username', 'password', 'first_name', 'middle_name', 'last_name', 'contact_number', 'age', 'weight', 'blood_type', 'health_condition')

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.individual_type = self.individual_type


class HospitalForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    type = 'O'
    name = forms.CharField(widget=forms.TextInput())
    address = forms.CharField(widget=forms.TextInput())
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '09XXXXXXXXX'}), error_messages={'invalid': 'Please enter a valid contact number (09XXXXXXXXX).'})
    org_type = 'H'

    class Meta:
        model = Hospital
        fields = ['username', 'password', 'name', 'address', 'contact_number']

    def __init__(self, *args, **kwargs):
        super(HospitalForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.org_type = self.org_type


class BloodBankForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    type = 'O'
    name = forms.CharField(widget=forms.TextInput())
    address = forms.CharField(widget=forms.TextInput())
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '09XXXXXXXXX'}), error_messages={'invalid': 'Please enter a valid contact number (09XXXXXXXXX).'})
    org_type = 'B'

    class Meta:
        model = BloodBank
        fields = ['username', 'password', 'name', 'address', 'contact_number']

    def __init__(self, *args, **kwargs):
        super(BloodBankForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.org_type = self.org_type

