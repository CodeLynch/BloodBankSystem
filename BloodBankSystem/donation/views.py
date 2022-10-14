from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from accounts.models import Donation, BloodBank, Donor, BloodSupply, User
from donation.forms import DonationForm
from django.db import IntegrityError


class DonationView(View):
    template = 'donation_index.html'

    def get(self, request):
        user = User.objects.get(username=request.session['username'])
        form = DonationForm()
        blood_banks = BloodBank.objects.exclude(blood_supply_id=None)
        return render(request, self.template, {'form': form, 'blood_banks': blood_banks, 'user_image': user.image_tag})

    def post(self, request):
        form = DonationForm(request.POST)
        user_id = request.POST['blood_bank']
        if form.is_valid():
            # getting the blood bank object by its user_id and assigning it to blood_bank field
            try:
                blood_bank = BloodBank.objects.get(user_id=user_id)
                donation = form.save(commit=False)
                donation.blood_bank = blood_bank
                donation.status = 'Pending'

                # getting donor object through its username and assigning it to donor field
                donor = Donor.objects.get(username=request.session['username'])
                donation.donor = donor
                donation.save()

                messages.success(request, 'Donation recorded successfully!')
                return redirect(reverse('accounts:index'))

            except IntegrityError:
                messages.error(request, 'You can only donate once in a day.')
                return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})
