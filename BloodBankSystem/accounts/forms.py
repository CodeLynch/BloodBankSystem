from django import forms
from .models import *


class DonorForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput()),
    password = forms.CharField(widget=forms.PasswordInput()),
    type = 'I'
    first_name = forms.CharField(widget=forms.TextInput()),
    middle_name = forms.CharField(widget=forms.TextInput()),
    last_name = forms.CharField(widget=forms.TextInput()),
    contact_number = forms.CharField(widget=forms.TextInput()),
    age = forms.IntegerField(widget=forms.NumberInput()),
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
    username = forms.CharField(widget=forms.TextInput()),
    password = forms.CharField(widget=forms.PasswordInput()),
    type = 'I'
    first_name = forms.CharField(widget=forms.TextInput()),
    middle_name = forms.CharField(widget=forms.TextInput()),
    last_name = forms.CharField(widget=forms.TextInput()),
    contact_number = forms.CharField(widget=forms.TextInput()),
    age = forms.IntegerField(widget=forms.NumberInput()),
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
    contact_number = forms.CharField(widget=forms.TextInput())
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
    contact_number = forms.CharField(widget=forms.TextInput())
    org_type = 'B'

    class Meta:
        model = BloodBank
        fields = ['username', 'password', 'name', 'address', 'contact_number']

    def __init__(self, *args, **kwargs):
        super(BloodBankForm, self).__init__(*args, **kwargs)
        self.instance.type = self.type
        self.instance.org_type = self.org_type


'''class IndividualForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    type = 'I'
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    age = forms.IntegerField(widget=forms.NumberInput)
    weight = forms.FloatField(widget=forms.FloatField)
    contact_number = forms.CharField(widget=forms.TextInput)
    health_condition = forms.CharField(widget=forms.Textarea)
    blood_type = forms.CharField(widget=forms.Select)
    individual_type = forms.CharField(widget=forms.Select)

    class Meta:
        model = Individual
        fields = ['username', 'password', 'first_name', 'last_name', 'age', 'weight', 'contact_number',
                  'health_condition', 'blood_type', 'individual_type']


class OrganizationForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    type = 'O'
    name = forms.CharField(widget=forms.TextInput)
    address = forms.CharField(widget=forms.TextInput)
    contact_number = forms.CharField(widget=forms.TextInput)
    org_type = forms.CharField(widget=forms.Select)

    class Meta:
        model = Organization
        fields = ['username', 'password', 'name', 'address', 'contact_number', 'contact_number', 'org_type']


class BloodSupplyForm(ModelForm):
    aplus_amount = forms.IntegerField(widget=forms.NumberInput)
    amin_amount = forms.IntegerField(widget=forms.NumberInput)
    bplus_amount = forms.IntegerField(widget=forms.NumberInput)
    bmin_amount = forms.IntegerField(widget=forms.NumberInput)
    abplus_amount = forms.IntegerField(widget=forms.NumberInput)
    abmin_amount = forms.IntegerField(widget=forms.NumberInput)
    oplus_amount = forms.IntegerField(widget=forms.NumberInput)
    omin_amount = forms.IntegerField(widget=forms.NumberInput)

    class Meta:
        model = BloodSupply
        fields = ['aplus_amount', 'amin_amount', 'bplus_amount', 'bmin_amount',
                  'abplus_amount', 'abmin_amount', 'oplus_amount', 'omin_amount']


class DonationForm(ModelForm):
    donor = forms.CharField(widget=forms.ChoiceField)
    blood_bank = forms.CharField(widget=forms.ChoiceField)
    donation_date = forms.DateField(widget=forms.DateField)
    status = False

    class Meta:
        model = Donation
        fields = ['donor', 'blood_bank', 'donation_date']


class TransfusionForm(ModelForm):
    recipient = forms.CharField(widget=forms.ChoiceField)
    hospital = forms.ForeignKey(widget=forms.ChoiceField)
    transfusion_date = forms.DateField(widget=forms.DateField)
    status = False

    class Meta:
        model = Transfusion
        fields = ['recipient', 'hospital', 'transfusion_date']


class RequestForm(ModelForm):
    recipient = forms.CharField(widget=forms.ChoiceField)
    hospital = forms.ForeignKey(widget=forms.ChoiceField)
    transfusion_date = forms.DateField(widget=forms.DateField)
    status = False

    class Meta:
        model = Transfusion
        fields = ['recipient', 'hospital', 'transfusion_date']'''
