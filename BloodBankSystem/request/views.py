from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from request.forms import *
from accounts.models import BloodSupply

# Create your views here.


class RequestBloodSupplyView(View):
    template = 'request_blood_supply.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            form = RequestBloodSupplyForm
            return render(request, self.template, {'form': form})

    def post(self, request):
        form = RequestBloodSupplyForm(request.POST)
        blood_bank_id = request.POST['blood_bank'].split(":")[0]
        blood_bank = BloodBank.objects.get(pk=blood_bank_id)
        if form.is_valid():
            #get hospital object of current user and assign to hospital field
            hospital= Hospital.objects.get(username=request.session['username'])
            requestt = form.save(commit=False)
            requestt.hospital = hospital
            requestt.status = True
            # get blood supply of hospital and bloodban
            giver_blood_supply = BloodSupply.objects.get(pk=blood_bank.blood_supply_id)
            receiver_blood_supply = BloodSupply.objects.get(pk=request.session['blood_supply_id'])
            available = False
            # check if blood_type is available--------------------
            if request.POST['blood_type'] == 'A+':
                if giver_blood_supply.aplus_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Blood Bank has no A+ blood in their supply')
            elif request.POST['blood_type'] == 'A-':
                if giver_blood_supply.amin_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Blood Bank has no A- blood in their supply')
            elif request.POST['blood_type'] == 'B+':
                if giver_blood_supply.bplus_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Blood Bank has no B+ blood in their supply')
            elif request.POST['blood_type'] == 'B-':
                if giver_blood_supply.bmin_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Blood Bank has no B- blood in their supply')
            elif request.POST['blood_type'] == 'AB+':
                if giver_blood_supply.abplus_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Blood Bank has no AB+ blood in their supply')
            elif request.POST['blood_type'] == 'AB-':
                if giver_blood_supply.abmin_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Blood Bank has no AB- blood in their supply')
            elif request.POST['blood_type'] == 'O+':
                if giver_blood_supply.oplus_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Blood Bank has no O+ blood in their supply')
            else:
                if giver_blood_supply.omin_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Blood Bank has no O- blood in their supply')
            # ----------------------------------------------
            # update hospital and blood bank if available--------
            if available:
                if request.POST['blood_type'] == 'A+':
                    initVal = giver_blood_supply.aplus_amount
                    giver_blood_supply.aplus_amount = initVal - int(request.POST['quantity'])
                    initVal = receiver_blood_supply.aplus_amount
                    receiver_blood_supply.aplus_amount = initVal + int(request.POST['quantity'])
                    giver_blood_supply.save(update_fields=["aplus_amount"])
                    receiver_blood_supply.save(update_fields=["aplus_amount"])
                elif request.POST['blood_type'] == 'A-':
                    initVal = giver_blood_supply.amin_amount
                    giver_blood_supply.amin_amount = initVal - int(request.POST['quantity'])
                    initVal = receiver_blood_supply.amin_amount
                    receiver_blood_supply.amin_amount = initVal + int(request.POST['quantity'])
                    giver_blood_supply.save(update_fields=["amin_amount"])
                    receiver_blood_supply.save(update_fields=["amin_amount"])
                elif request.POST['blood_type'] == 'B+':
                    initVal = giver_blood_supply.bplus_amount
                    giver_blood_supply.bplus_amount = initVal - int(request.POST['quantity'])
                    initVal = receiver_blood_supply.bplus_amount
                    receiver_blood_supply.bplus_amount = initVal + int(request.POST['quantity'])
                    giver_blood_supply.save(update_fields=["bplus_amount"])
                    receiver_blood_supply.save(update_fields=["bplus_amount"])
                elif request.POST['blood_type'] == 'B-':
                    initVal = giver_blood_supply.bmin_amount
                    giver_blood_supply.bmin_amount = initVal - int(request.POST['quantity'])
                    initVal = receiver_blood_supply.bmin_amount
                    receiver_blood_supply.bmin_amount = initVal + int(request.POST['quantity'])
                    giver_blood_supply.save(update_fields=["bmin_amount"])
                    receiver_blood_supply.save(update_fields=["bmin_amount"])
                elif request.POST['blood_type'] == 'AB+':
                    initVal = giver_blood_supply.abplus_amount
                    giver_blood_supply.abplus_amount = initVal - int(request.POST['quantity'])
                    initVal = receiver_blood_supply.abplus_amount
                    receiver_blood_supply.abplus_amount = initVal + int(request.POST['quantity'])
                    giver_blood_supply.save(update_fields=["abplus_amount"])
                    receiver_blood_supply.save(update_fields=["abplus_amount"])
                elif request.POST['blood_type'] == 'AB-':
                    initVal = giver_blood_supply.abmin_amount
                    giver_blood_supply.abmin_amount = initVal - int(request.POST['quantity'])
                    initVal = receiver_blood_supply.abmin_amount
                    receiver_blood_supply.abmin_amount = initVal + int(request.POST['quantity'])
                    giver_blood_supply.save(update_fields=["abmin_amount"])
                    receiver_blood_supply.save(update_fields=["abmin_amount"])
                elif request.POST['blood_type'] == 'O+':
                    initVal = giver_blood_supply.oplus_amount
                    giver_blood_supply.oplus_amount = initVal - int(request.POST['quantity'])
                    initVal = receiver_blood_supply.oplus_amount
                    receiver_blood_supply.oplus_amount = initVal + int(request.POST['quantity'])
                    giver_blood_supply.save(update_fields=["oplus_amount"])
                    receiver_blood_supply.save(update_fields=["oplus_amount"])
                else:
                    initVal = giver_blood_supply.omin_amount
                    giver_blood_supply.omin_amount = initVal - int(request.POST['quantity'])
                    initVal = receiver_blood_supply.omin_amount
                    receiver_blood_supply.omin_amount = initVal + int(request.POST['quantity'])
                    giver_blood_supply.save(update_fields=["omin_amount"])
                    receiver_blood_supply.save(update_fields=["omin_amount"])
            # ----------------------------------------------
                requestt.save()
                messages.success(request, 'Blood supply requested successfully!')
                return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})