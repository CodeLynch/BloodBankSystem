from django.db import models
from django.core.validators import RegexValidator

contact_number_validator = RegexValidator(regex= r'^(09|\+639)\d{9}$')


class User(models.Model):
    type_user = (('I', 'Individual'), ('O', 'Organization'))
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=1, choices=type_user)


class Individual(User):
    type_individual = (('D', 'Donor'), ('R', 'Recipient'))
    type_blood = (('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'),
                  ('AB-', 'AB-'), ('O-', 'O-'))
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField(verbose_name='Weight (kg)')
    contact_number = models.CharField(max_length=13, validators=[contact_number_validator])
    health_condition = models.TextField(max_length=50, null=True, blank=True, verbose_name='Health conditions (optional)')
    blood_type = models.CharField(max_length=3, choices=type_blood)
    individual_type = models.CharField(max_length=1, choices=type_individual)

    def __str__(self):
        return '%s: %s %s' % (self.user_id, self.first_name, self.last_name)


class BloodSupply(models.Model):
    supply_id = models.AutoField(primary_key=True)
    aplus_amount = models.IntegerField(default=0)
    amin_amount = models.IntegerField(default=0)
    bplus_amount = models.IntegerField(default=0)
    bmin_amount = models.IntegerField(default=0)
    abplus_amount = models.IntegerField(default=0)
    abmin_amount = models.IntegerField(default=0)
    oplus_amount = models.IntegerField(default=0)
    omin_amount = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.supply_id)


class Organization(User):
    type_organization = (('H', 'Hospital'), ('B', 'Blood Bank'))
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=13, validators=[contact_number_validator])
    blood_supply = models.ForeignKey(BloodSupply, null=True, on_delete=models.SET_NULL)
    org_type = models.CharField(max_length=1, choices=type_organization)

    def __str__(self):
        return '%s: %s' % (self.user_id, self.name)


class Donor(Individual):
    pass


class Recipient(Individual):
    pass


class Hospital(Organization):
    pass


class BloodBank(Organization):
    pass


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    donation_date = models.DateField()
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('donor', 'donation_date')


class Transfusion(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    transfusion_date = models.DateField()
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('recipient', 'transfusion_date')


class Request(models.Model):
    type_blood = (('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'),
                  ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-'))
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    blood_type = models.CharField(max_length=3, choices=type_blood)
    quantity = models.IntegerField(default=0)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

