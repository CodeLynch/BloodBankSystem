from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from accounts.models import Recipient, Hospital, BloodSupply
from transfusion.forms import TransfusionForm
from django.db import IntegrityError

# Create your views here.


class TransfusionView(View):
    template = 'transfusion_index.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            form = TransfusionForm()
            return render(request, self.template, {'form': form})

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
            available = False
            #check if blood_type is available--------------------
            if request.session['blood_type'] == 'A+':
                if blood_supply.aplus_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Hospital has no A+ blood in their supply')
            elif request.session['blood_type'] == 'A-':
                if blood_supply.amin_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Hospital has no A- blood in their supply')
            elif request.session['blood_type'] == 'B+':
                if blood_supply.bplus_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Hospital has no B+ blood in their supply')
            elif request.session['blood_type'] == 'B-':
                if blood_supply.bmin_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Hospital has no B- blood in their supply')
            elif request.session['blood_type'] == 'AB+':
                if blood_supply.abplus_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Hospital has no AB+ blood in their supply')
            elif request.session['blood_type'] == 'AB-':
                if blood_supply.abmin_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Hospital has no AB- blood in their supply')
            elif request.session['blood_type'] == 'O+':
                if blood_supply.oplus_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Hospital has no O+ blood in their supply')
            else:
                if blood_supply.omin_amount > 0:
                    available = True
                else:
                    messages.error(request, 'Hospital has no O- blood in their supply')
            # update base on blood_type if available--------
            try:
                if available:
                    transfusion.save()
                    if request.session['blood_type'] == 'A+':
                        initVal = blood_supply.aplus_amount
                        blood_supply.aplus_amount = initVal - 1
                        blood_supply.save(update_fields=["aplus_amount"])
                    elif request.session['blood_type'] == 'A-':
                        initVal = blood_supply.amin_amount
                        blood_supply.amin_amount = initVal - 1
                        blood_supply.save(update_fields=["amin_amount"])
                    elif request.session['blood_type'] == 'B+':
                        initVal = blood_supply.bplus_amount
                        blood_supply.bplus_amount = initVal - 1
                        blood_supply.save(update_fields=["bplus_amount"])
                    elif request.session['blood_type'] == 'B-':
                        initVal = blood_supply.bmin_amount
                        blood_supply.bmin_amount = initVal - 1
                        blood_supply.save(update_fields=["bmin_amount"])
                    elif request.session['blood_type'] == 'AB+':
                        initVal = blood_supply.abplus_amount
                        blood_supply.abplus_amount = initVal - 1
                        blood_supply.save(update_fields=["abplus_amount"])
                    elif request.session['blood_type'] == 'AB-':
                        initVal = blood_supply.abmin_amount
                        blood_supply.abmin_amount = initVal - 1
                        blood_supply.save(update_fields=["abmin_amount"])
                    elif request.session['blood_type'] == 'O+':
                        initVal = blood_supply.oplus_amount
                        blood_supply.oplus_amount = initVal - 1
                        blood_supply.save(update_fields=["oplus_amount"])
                    else:
                        initVal = blood_supply.omin_amount
                        blood_supply.omin_amount = initVal - 1
                        blood_supply.save(update_fields=["omin_amount"])
                # ----------------------------------------------
                    messages.success(request, 'Transfusion recorded successfully!')
                    return redirect(reverse('accounts:index'))
            except IntegrityError:
                messages.error(request, "You can only receive transfusion once in a day")
                return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})
