from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from accounts.models import Donation, BloodBank
from donation.forms import DonationForm

# Create your views here.

class DonationView(View):
    template = 'donation_index.html'

    def get(self, request):
        form = DonationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = DonationForm(request.POST)
        user_id = request.POST['bloodbank'].split(":")[0]
        if form.is_valid():
            bloodbank = BloodBank.objects.get(user_id=user_id)
            donation = form.save(commit=False)
            donation.bloodbank = bloodbank
            donation.status = True
            from BloodBankSystem.accounts.models import Donor
            donor = Donor.objects.get(username=request.session['username'])
            donation.donor = donor
            donation.save()
            messages.success(request, 'Transfusion Recorded Successfully!')
            return redirect(reverse('accounts:index'))
        return redirect(reverse('accounts:index'))

