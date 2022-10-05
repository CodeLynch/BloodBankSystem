from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from accounts.models import Donation, BloodBank, Donor, BloodSupply
from donation.forms import DonationForm
from django.db import IntegrityError


def is_approved(blood_supply, field_name):
    init_value = getattr(blood_supply, field_name)
    setattr(blood_supply, field_name, init_value + 1)
    blood_supply.save(update_fields=[field_name])
    return True


class DonationView(View):
    template = 'donation_index.html'

    def get(self, request):
        form = DonationForm()
        blood_banks = BloodBank.objects.exclude(blood_supply_id=None)
        return render(request, self.template, {'form': form, 'blood_banks': blood_banks})

    def post(self, request):
        form = DonationForm(request.POST)
        user_id = request.POST['blood_bank'].split(":")[0]
        if form.is_valid():
            # getting the blood bank object by its user_id and assigning it to blood_bank field
            try:
                blood_bank = BloodBank.objects.get(user_id=user_id)
                donation = form.save(commit=False)
                donation.blood_bank = blood_bank
                donation.status = True
                
                # getting donor object through its username and assigning it to donor field
                donor = Donor.objects.get(username=request.session['username'])
                donation.donor = donor
                donation.save()
                
                # update blood supply of blood bank
                blood_supply = BloodSupply.objects.get(pk=blood_bank.blood_supply_id)

                # update base on blood_type--------------------
                if request.session['blood_type'] == 'A+':
                    approved = is_approved(blood_supply, 'aplus_amount')
                elif request.session['blood_type'] == 'A-':
                    approved = is_approved(blood_supply, 'amin_amount')
                elif request.session['blood_type'] == 'B+':
                    approved = is_approved(blood_supply, 'bplus_amount')
                elif request.session['blood_type'] == 'B-':
                    approved = is_approved(blood_supply, 'bmin_amount')
                elif request.session['blood_type'] == 'AB+':
                    approved = is_approved(blood_supply, 'abplus_amount')
                elif request.session['blood_type'] == 'AB-':
                    approved = is_approved(blood_supply, 'abmin_amount')
                elif request.session['blood_type'] == 'O+':
                    approved = is_approved(blood_supply, 'oplus_amount')
                else:
                    approved = is_approved(blood_supply, 'omin_amount')
                #----------------------------------------------
                
                if approved:
                    messages.success(request, 'Donation recorded successfully!')
                    return redirect(reverse('accounts:index'))
            except IntegrityError:
                messages.error(request, 'You can only donate once in a day.')
                return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})

