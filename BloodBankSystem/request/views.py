from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from request.forms import *


class RequestBloodSupplyView(View):
    template = 'request_blood_supply.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            user = User.objects.get(username=request.session['username'])
            form = RequestBloodSupplyForm
            blood_banks = BloodBank.objects.exclude(blood_supply_id=None)
            return render(request, self.template, {'form': form, 'blood_banks': blood_banks, 'user_image': user.image_tag})

    def post(self, request):
        user = User.objects.get(username=request.session['username'])
        blood_banks = BloodBank.objects.exclude(blood_supply_id=None)
        form = RequestBloodSupplyForm(request.POST)
        blood_bank_id = request.POST['blood_bank']
        blood_bank = BloodBank.objects.get(pk=blood_bank_id)
        if form.is_valid():
            # get hospital object of current user and assign to hospital field
            hospital = Hospital.objects.get(username=request.session['username'])
            requestt = form.save(commit=False)
            requestt.hospital = hospital
            requestt.status = 'Pending'
            quantity = int(request.POST['quantity'])

            requestt.save()
            messages.success(request, 'Blood supply request sent successfully!')
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form, 'blood_banks': blood_banks, 'user_image': user.image_tag})
