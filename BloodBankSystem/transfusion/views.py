from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from accounts.models import Recipient, Hospital, BloodSupply, Transfusion, User
from transfusion.forms import TransfusionForm
from django.db import IntegrityError


def is_available(blood_supply, blood_type):
    init_value = 0
    if blood_type == 'A+':
        init_value = getattr(blood_supply, 'aplus_amount')
    elif blood_type == 'B+':
        init_value = getattr(blood_supply, 'bplus_amount')
    elif blood_type == 'AB+':
        init_value = getattr(blood_supply, 'abplus_amount')
    elif blood_type == 'O+':
        init_value = getattr(blood_supply, 'oplus_amount')
    elif blood_type == 'A-':
        init_value = getattr(blood_supply, 'amin_amount')
    elif blood_type == 'B-':
        init_value = getattr(blood_supply, 'bmin_amount')
    elif blood_type == 'AB-':
        init_value = getattr(blood_supply, 'abmin_amount')
    else:
        init_value = getattr(blood_supply, 'omin_amount')

    if init_value > 0:
        return True
    else:
        return False


def update_blood_supply(blood_supply, blood_type):
    field_name=''
    if blood_type == 'A+':
        init_value = getattr(blood_supply, 'aplus_amount')
        field_name = 'aplus_amount'
    elif blood_type == 'B+':
        init_value = getattr(blood_supply, 'bplus_amount')
        field_name = 'bplus_amount'
    elif blood_type == 'AB+':
        init_value = getattr(blood_supply, 'abplus_amount')
        field_name = 'abplus_amount'
    elif blood_type == 'O+':
        init_value = getattr(blood_supply, 'oplus_amount')
        field_name = 'oplus_amount'
    elif blood_type == 'A-':
        init_value = getattr(blood_supply, 'amin_amount')
        field_name = 'amin_amount'
    elif blood_type == 'B-':
        init_value = getattr(blood_supply, 'bmin_amount')
        field_name = 'bmin_amount'
    elif blood_type == 'AB-':
        init_value = getattr(blood_supply, 'abmin_amount')
        field_name = 'abmin_amount'
    else:
        init_value = getattr(blood_supply, 'omin_amount')
        field_name = 'omin_amount'

    setattr(blood_supply, field_name, init_value - 1)
    blood_supply.save(update_fields=[field_name])
    return True


class TransfusionView(View):
    template = 'transfusion_index.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            user = User.objects.get(username=request.session['username'])
            form = TransfusionForm(request.session['blood_type'])
            hospitals = Hospital.objects.exclude(blood_supply_id=None)
            return render(request, self.template, {'form': form, 'hospitals': hospitals, 'user_image': user.image_tag})

    def post(self, request):
        form = TransfusionForm(request.session['blood_type'], request.POST)
        user_id = request.POST['hospital']
        if form.is_valid():
            # getting the hospital object by its user_id and assigning it to hospital field
            blood_type = request.POST.get('requested_blood_type')
            hospital = Hospital.objects.get(pk=user_id)
            # get blood supply of hospital
            blood_supply = BloodSupply.objects.get(pk=hospital.blood_supply_id)

            try:
                if is_available(blood_supply, blood_type):
                    transfusion = form.save(commit=False)
                    transfusion.hospital = hospital
                    transfusion.status = 'Pending'
                    recipient = Recipient.objects.get(username=request.session['username'])
                    transfusion.recipient = recipient
                    transfusion.requested_blood_type = blood_type
                    transfusion.save()
                    messages.success(request, 'Transfusion request sent!')
                else:
                    messages.error(request, 'Hospital has no ' + blood_type + ' blood in their supply.')
                return redirect(reverse('accounts:index'))
            except IntegrityError:
                messages.error(request, "You can only receive transfusion once in a day.")
                return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})


def update_transfusion(request, id):
    if request.method == 'POST':
        if 'A' in request.POST:
            transfusion = Transfusion.objects.get(pk=id)
            try:
                blood_type = transfusion.requested_blood_type
                hospital = transfusion.hospital
                blood_supply = BloodSupply.objects.get(pk=hospital.blood_supply_id)
                if is_available(blood_supply, blood_type):
                    if update_blood_supply(blood_supply, blood_type):
                        setattr(transfusion, 'status', 'Approved')
                        transfusion.save(update_fields=['status'])
                        messages.success(request, 'Transfusion request granted!')
                else:
                    messages.error(request, 'You have no ' + blood_type + ' blood in your supply.')
            except BloodSupply.DoesNotExist:
                messages.error(request, 'No existing blood supply!')
        elif 'D' in request.POST:
            transfusion = Transfusion.objects.get(pk=id)
            setattr(transfusion, 'status', 'Declined')
            transfusion.save(update_fields=['status'])

    return redirect(reverse('accounts:index'))
