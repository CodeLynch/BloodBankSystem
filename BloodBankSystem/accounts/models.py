from django.db import models
from django.core.validators import RegexValidator
from django.utils.html import mark_safe
from datetime import datetime
from PIL import Image
import os, random


contact_number_validator = RegexValidator(regex= r'^(09|\+639)\d{9}$')


def image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(char)) for x in range(10))
    now = datetime.now()
    return 'user_image/{year}-{month}-{day}-{image_id}-{base_name}-{randstr}{ext}'.format(image_id=instance, base_name=base_filename, randstr=randomstr, ext=file_extension, year=now.strftime('%Y'), month=now.strftime('%m'), day=now.strftime('%d'))

    
class User(models.Model):
    type_user = (('I', 'Individual'), ('O', 'Organization'))
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    user_image = models.ImageField(default='default.png', upload_to=image_path, verbose_name='Profile picture')
    type = models.CharField(max_length=1, choices=type_user)

    def __str__(self):
        return self.username

    def image_tag(self):
        return mark_safe('<img src="/media/%s" class="rounded-circle border" width="45" height="45"/>'%(self.user_image))

    def set_to_default(self):
        self.user_image = 'default.png'
        self.save()

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.user_image.path)
        width, height = img.size

        if width > 300 and height > 300:
            img.thumbnail((width, height))

        if height < width:
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))
        elif width < height:
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))
            
        img.save(self.user_image.path)
        

class Individual(User):
    type_individual = (('D', 'Donor'), ('R', 'Recipient'))
    type_blood = (('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-'))
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
    aplus_amount = models.IntegerField(default=0, verbose_name='A+ amount')
    amin_amount = models.IntegerField(default=0, verbose_name='A- amount')
    bplus_amount = models.IntegerField(default=0, verbose_name='B+ amount')
    bmin_amount = models.IntegerField(default=0, verbose_name='B- amount')
    abplus_amount = models.IntegerField(default=0, verbose_name='AB+ amount')
    abmin_amount = models.IntegerField(default=0, verbose_name='AB- amount')
    oplus_amount = models.IntegerField(default=0, verbose_name='O+ amount')
    omin_amount = models.IntegerField(default=0, verbose_name='O- amount')

    class Meta:
        verbose_name_plural = 'Blood Supplies'

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
    class Meta:
        verbose_name_plural = 'Blood Banks'


class Donation(models.Model):
    status_choices = (('Pending','Pending'),('Accepted','Accepted'),('Declined','Declined'))
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    donation_date = models.DateField()
    status = models.CharField(max_length=10, choices=status_choices)

    class Meta:
        unique_together = ('donor', 'donation_date')

    def __str__(self):
        return '%s on %s' % (self.donor, self.donation_date)


class Transfusion(models.Model):
    status_choices = (('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'))
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    transfusion_date = models.DateField()
    status = models.CharField(max_length=10, choices=status_choices)
    requested_blood_type = models.CharField(max_length=3)

    class Meta:
        unique_together = ('recipient', 'transfusion_date')

    def __str__(self):
        return '%s on %s' % (self.recipient, self.transfusion_date)


class Request(models.Model):
    status_choices = (('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'))
    type_blood = (('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-'))
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    blood_type = models.CharField(max_length=3, choices=type_blood)
    quantity = models.IntegerField(default=0)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices)

    def __str__(self):
        return 'Requested by %s to %s on %s' % (self.hospital, self.blood_bank, self.request_date)
