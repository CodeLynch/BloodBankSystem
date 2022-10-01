from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import *


# Create your views here.
class CreateBloodSupplyView(View):
    template = 'create_blood_supply.html'

    def get(self, request):
        form = CreateBloodSupplyForm
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = CreateBloodSupplyForm(request.POST)
        if form.is_valid():
            form.save()

            org = Organization.objects.get(username=request.session['username'])
            new_supply = BloodSupply.objects.latest('supply_id')
            org.blood_supply = new_supply
            org.save(update_fields=["blood_supply"])
            request.session['blood_supply_id'] = org.blood_supply_id
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})


class UpdateBloodSupplyView(View):
    template = 'update_blood_supply.html'

    def get(self, request):
        bloodSupply = BloodSupply.objects.get(pk=request.session['blood_supply_id'])
        form = UpdateBloodSupplyForm(instance=bloodSupply)
        return render(request, self.template, {'form': form})

    def post(self, request):
        bloodSupply = BloodSupply.objects.get(pk=request.session['blood_supply_id'])
        form = UpdateBloodSupplyForm(request.POST, instance=bloodSupply)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})


class DeleteBloodSupplyView(View):

    def get(self, request):
        owned_supply = BloodSupply.objects.get(pk=request.session['blood_supply_id'])
        owned_supply.delete()
        request.session['blood_supply_id'] = None
        return redirect(reverse('accounts:index'))