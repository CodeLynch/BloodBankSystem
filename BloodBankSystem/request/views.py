from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from request.forms import *
from accounts.models import BloodSupply


def is_approved(giver_supply, receiver_supply, field_name, quantity):
    giver_init_value = getattr(giver_supply, field_name)
    if giver_init_value >= quantity:
        receiver_init_value = getattr(receiver_supply, field_name)
        setattr(giver_supply, field_name, giver_init_value - quantity)
        setattr(receiver_supply, field_name, receiver_init_value + quantity)
        giver_supply.save(update_fields=[field_name])
        receiver_supply.save(update_fields=[field_name])
        return True
    else:
        return False


class RequestBloodSupplyView(View):
    template = 'request_blood_supply.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            form = RequestBloodSupplyForm
            blood_banks = BloodBank.objects.exclude(blood_supply_id=None)
            return render(request, self.template, {'form': form, 'blood_banks': blood_banks})

    def post(self, request):
        form = RequestBloodSupplyForm(request.POST)
        blood_bank_id = request.POST['blood_bank'].split(":")[0]
        blood_bank = BloodBank.objects.get(pk=blood_bank_id)
        if form.is_valid():
            # get hospital object of current user and assign to hospital field
            hospital = Hospital.objects.get(username=request.session['username'])
            requestt = form.save(commit=False)
            requestt.hospital = hospital
            requestt.status = True
            
            # get blood supply of hospital and bloodbank
            giver_blood_supply = BloodSupply.objects.get(pk=blood_bank.blood_supply_id)
            receiver_blood_supply = BloodSupply.objects.get(pk=request.session['blood_supply_id'])
            quantity = int(request.POST['quantity'])

            # update hospital and blood bank supply if available--------
            if request.POST['blood_type'] == 'A+':
                approved = is_approved(giver_blood_supply, receiver_blood_supply, 'aplus_amount', quantity)
                type = 'A+'
            elif request.POST['blood_type'] == 'A-':
                approved = is_approved(giver_blood_supply, receiver_blood_supply, 'amin_amount', quantity)
                type = 'A-'
            elif request.POST['blood_type'] == 'B+':
                approved = is_approved(giver_blood_supply, receiver_blood_supply, 'bplus_amount', quantity)
                type = 'B+'
            elif request.POST['blood_type'] == 'B-':
                iapproved = is_approved(giver_blood_supply, receiver_blood_supply, 'bmin_amount', quantity)
                type = 'B-'
            elif request.POST['blood_type'] == 'AB+':
                approved = is_approved(giver_blood_supply, receiver_blood_supply, 'abplus_amount', quantity)
                type = 'AB+'
            elif request.POST['blood_type'] == 'AB-':
                approved = is_approved(giver_blood_supply, receiver_blood_supply, 'abmin_amount', quantity)
                type = 'AB-'
            elif request.POST['blood_type'] == 'O+':
                approved = is_approved(giver_blood_supply, receiver_blood_supply, 'oplus_amount', quantity)
                type = 'O+'
            else:
                approved = is_approved(giver_blood_supply, receiver_blood_supply, 'omin_amount', quantity)
                type = 'O-'
            # ----------------------------------------------------------
            
            if approved:
                request.save()
                messages.success(request, 'Blood supply requested successfully!')
            else:
                messages.error(request, 'Blood Bank does not have sufficient ' + type + ' blood in their supply.')
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})