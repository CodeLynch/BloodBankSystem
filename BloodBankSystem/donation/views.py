from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from accounts.models import Donation, BloodBank, Donor, BloodSupply
from donation.forms import DonationForm

# Create your views here.


class DonationView(View):
    template = 'donation_index.html'

    def get(self, request):
        form = DonationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = DonationForm(request.POST)
        user_id = request.POST['blood_bank'].split(":")[0]
        if form.is_valid():
            #getting the blood bank object by its user_id and assigning it to blood_bank field
            blood_bank = BloodBank.objects.get(user_id=user_id)
            donation = form.save(commit=False)
            donation.blood_bank = blood_bank
            donation.status = True
            #getting donor object through its username and assigning it to donor field
            donor = Donor.objects.get(username=request.session['username'])
            donation.donor = donor
            donation.save()
            #update blood supply of blood bank
            blood_supply = BloodSupply.objects.get(pk=blood_bank.blood_supply_id)
            #update base on blood_type--------------------
            if request.session['blood_type'] == 'A+':
                initVal = blood_supply.aplus_amount
                blood_supply.aplus_amount = initVal + 1
                blood_supply.save(update_fields=["aplus_amount"])
            elif request.session['blood_type'] == 'A-':
                initVal = blood_supply.amin_amount
                blood_supply.amin_amount = initVal + 1
                blood_supply.save(update_fields=["amin_amount"])
            elif request.session['blood_type'] == 'B+':
                initVal = blood_supply.bplus_amount
                blood_supply.bplus_amount = initVal + 1
                blood_supply.save(update_fields=["bplus_amount"])
            elif request.session['blood_type'] == 'B-':
                initVal = blood_supply.bmin_amount
                blood_supply.bmin_amount = initVal + 1
                blood_supply.save(update_fields=["bmin_amount"])
            elif request.session['blood_type'] == 'AB+':
                initVal = blood_supply.abplus_amount
                blood_supply.abplus_amount = initVal + 1
                blood_supply.save(update_fields=["abplus_amount"])
            elif request.session['blood_type'] == 'AB-':
                initVal = blood_supply.abmin_amount
                blood_supply.abmin_amount = initVal + 1
                blood_supply.save(update_fields=["abmin_amount"])
            elif request.session['blood_type'] == 'O+':
                initVal = blood_supply.oplus_amount
                blood_supply.oplus_amount = initVal + 1
                blood_supply.save(update_fields=["oplus_amount"])
            else:
                initVal = blood_supply.omin_amount
                blood_supply.omin_amount = initVal + 1
                blood_supply.save(update_fields=["omin_amount"])
            #----------------------------------------------

            messages.success(request, 'Donation recorded successfully!')
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})

