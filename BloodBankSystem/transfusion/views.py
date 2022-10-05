from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from accounts.models import Recipient, Hospital, BloodSupply
from transfusion.forms import TransfusionForm
from django.db import IntegrityError


def is_approved(blood_supply, field_name):
    init_value = getattr(blood_supply, field_name)
    if init_value > 0:
        setattr(blood_supply, field_name, init_value - 1)
        blood_supply.save(update_fields=[field_name])
        return True
    else:
        return False


class TransfusionView(View):
    template = 'transfusion_index.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            form = TransfusionForm()
            hospitals = Hospital.objects.exclude(blood_supply_id=None)
            return render(request, self.template, {'form': form, 'hospitals': hospitals})

    def post(self, request):
        form = TransfusionForm(request.POST)
        user_id = request.POST['hospital']
        if form.is_valid():
            # getting the hospital object by its user_id and assigning it to hospital field
            hospital = Hospital.objects.get(user_id=user_id)
            transfusion = form.save(commit=False)
            transfusion.hospital = hospital
            transfusion.status = True
            
            # getting donor object through its username and assigning it to donor field
            recipient = Recipient.objects.get(username=request.session['username'])
            transfusion.recipient = recipient
            
            # get blood supply of hospital
            blood_supply = BloodSupply.objects.get(pk=hospital.blood_supply_id)
            
            # update base on blood_type if available--------
            if request.session['blood_type'] == 'A+':
                approved = is_approved(blood_supply, 'aplus_amount')
                type = 'A+'
            elif request.session['blood_type'] == 'A-':
                approved = is_approved(blood_supply, 'amin_amount')
                type = 'A-'
            elif request.session['blood_type'] == 'B+':
                approved = is_approved(blood_supply, 'bplus_amount')
                type = 'B+'
            elif request.session['blood_type'] == 'B-':
                approved = is_approved(blood_supply, 'bmin_amount')
                type = 'B-'
            elif request.session['blood_type'] == 'AB+':
                approved = is_approved(blood_supply, 'abplus_amount')
                type = 'AB+'
            elif request.session['blood_type'] == 'AB-':
                approved = is_approved(blood_supply, 'abmin_amount')
                type = 'AB-'
            elif request.session['blood_type'] == 'O+':
                approved = is_approved(blood_supply, 'oplus_amount')
                type = 'O+'
            else:
                approved = is_approved(blood_supply, 'omin_amount')
                type = 'O-'
            # ----------------------------------------------

            try:
                if approved:
                    transfusion.save()
                    messages.success(request, 'Transfusion recorded successfully!')
                else:
                    messages.error(request, 'Hospital has no ' + type + ' blood in their supply.')
                return redirect(reverse('accounts:index'))
            except IntegrityError:
                messages.error(request, "You can only receive transfusion once in a day.")
                return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})
