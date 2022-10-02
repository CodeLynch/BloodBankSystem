from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from accounts.models import Donation, BloodBank, Donor
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
            blood_bank = BloodBank.objects.get(user_id=user_id)
            donation = form.save(commit=False)
            donation.blood_bank = blood_bank
            donation.status = True
            donor = Donor.objects.get(username=request.session['username'])
            donation.donor = donor
            donation.save()
            messages.success(request, 'Donation recorded successfully!')
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})

