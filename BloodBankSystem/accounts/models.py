from django.db import models


# Create your models here.
class User(models.Model):
    type_user = (('I', 'Individual'), ('O', 'Organization'))
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=1, choices=type_user)


class Individual(User):
    type_individual = (('D', 'Donor'), ('R', 'Recipient'))
    type_blood = (('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'),
                  ('AB-', 'AB-'), ('O-', 'O-'))
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    weight = models.FloatField()
    contact_number = models.CharField(max_length=11)
    health_condition = models.CharField(max_length=20, null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=type_blood)
    individual_type = models.CharField(max_length=1, choices=type_individual)


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


class Organization(User):
    type_organization = (('H', 'Hospital'), ('B', 'Blood Bank'))
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=11)
    blood_supply = models.ForeignKey(BloodSupply, on_delete=models.CASCADE)
    org_type = models.CharField(max_length=1, choices=type_organization)


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

