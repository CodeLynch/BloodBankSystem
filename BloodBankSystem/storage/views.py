from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from storage.forms import *
from accounts.models import Donation, BloodBank, BloodSupply, Request, Hospital


def is_approved(blood_supply, field_name):
    init_value = getattr(blood_supply, field_name)
    setattr(blood_supply, field_name, init_value + 1)
    blood_supply.save(update_fields=[field_name])
    return True


def request_is_approved(giver_supply, receiver_supply, field_name, quantity):
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


# Create your views here.
class CreateBloodSupplyView(View):
    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            new_blood_supply = BloodSupply(aplus_amount=0,
                                           amin_amount=0,
                                           bplus_amount=0,
                                           bmin_amount=0,
                                           abplus_amount=0,
                                           abmin_amount=0,
                                           oplus_amount=0,
                                           omin_amount=0)
            new_blood_supply.save()
            org = Organization.objects.get(username=request.session['username'])
            new_supply = BloodSupply.objects.latest('supply_id')
            org.blood_supply = new_supply
            org.save(update_fields=["blood_supply"])
            request.session['blood_supply_id'] = org.blood_supply_id
            messages.success(request, 'Blood supply created successfully!')
        return redirect(reverse('accounts:index'))


class UpdateBloodSupplyView(View):
    template = 'update_blood_supply.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            user = User.objects.get(username=request.session['username'])
            bloodSupply = BloodSupply.objects.get(pk=request.session['blood_supply_id'])
            form = BloodSupplyForm(instance=bloodSupply)
            return render(request, self.template, {'form': form, 'user_image': user.image_tag})

    def post(self, request):
        bloodSupply = BloodSupply.objects.get(pk=request.session['blood_supply_id'])
        form = BloodSupplyForm(request.POST, instance=bloodSupply)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood supply updated successfully!')
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})


class DeleteBloodSupplyView(View):

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            owned_supply = BloodSupply.objects.get(pk=request.session['blood_supply_id'])
            owned_supply.delete()
            request.session['blood_supply_id'] = None
            messages.success(request, 'Blood supply deleted successfully.')
            return redirect(reverse('accounts:index'))


def update_donation(request, id):
    if request.method == 'POST':
        if 'A' in request.POST:
            if request.session['blood_supply_id'] is None:
                messages.error(request, 'You do not have a blood supply')
            else:
                donation = Donation.objects.get(pk=id)
                setattr(donation, 'status', 'Accepted')
                donation.save(update_fields=['status'])

                # get blood type, blood supply of user
                blood_type = donation.donor.blood_type
                blood_supplyID = request.session['blood_supply_id']
                blood_supply = BloodSupply.objects.get(pk=blood_supplyID)
                # update base on blood_type--------------------
                if blood_type == 'A+':
                    approved = is_approved(blood_supply, 'aplus_amount')
                elif blood_type == 'A-':
                    approved = is_approved(blood_supply, 'amin_amount')
                elif blood_type == 'B+':
                    approved = is_approved(blood_supply, 'bplus_amount')
                elif blood_type == 'B-':
                    approved = is_approved(blood_supply, 'bmin_amount')
                elif blood_type == 'AB+':
                    approved = is_approved(blood_supply, 'abplus_amount')
                elif blood_type == 'AB-':
                    approved = is_approved(blood_supply, 'abmin_amount')
                elif blood_type == 'O+':
                    approved = is_approved(blood_supply, 'oplus_amount')
                else:
                    approved = is_approved(blood_supply, 'omin_amount')
                # ----------------------------------------------
                if approved:
                    messages.success(request, 'Blood Bank updated!')
        elif 'D' in request.POST:
            donation = Donation.objects.get(pk=id)
            setattr(donation, 'status', 'Declined')
            donation.save(update_fields=['status'])

    return redirect(reverse('accounts:index'))


def update_request(request, id):
    if request.method == 'POST':
        if 'A' in request.POST:
            request_o = Request.objects.get(pk=id)
            if request.session['blood_supply_id'] is None:
                messages.error(request, 'You do not have a blood supply')
            elif request_o.hospital.blood_supply is None:
                messages.error(request, request_o.hospital.name + ' has removed their blood supply')
            else:
                # get blood type, quantity, and blood supply of giver and receiver
                blood_type = request_o.blood_type
                quantity = request_o.quantity
                giver_supplyID = request.session['blood_supply_id']
                receiver_supplyID = request_o.hospital.blood_supply.supply_id
                giver_blood_supply = BloodSupply.objects.get(pk=giver_supplyID)
                receiver_blood_supply = BloodSupply.objects.get(pk=receiver_supplyID)

                # update hospital and blood bank supply if available--------
                if blood_type == 'A+':
                    approved = request_is_approved(giver_blood_supply, receiver_blood_supply, 'aplus_amount', quantity)
                    type = 'A+'
                elif blood_type == 'A-':
                    approved = request_is_approved(giver_blood_supply, receiver_blood_supply, 'amin_amount', quantity)
                    type = 'A-'
                elif blood_type == 'B+':
                    approved = request_is_approved(giver_blood_supply, receiver_blood_supply, 'bplus_amount', quantity)
                    type = 'B+'
                elif blood_type == 'B-':
                    approved = request_is_approved(giver_blood_supply, receiver_blood_supply, 'bmin_amount', quantity)
                    type = 'B-'
                elif blood_type == 'AB+':
                    approved = request_is_approved(giver_blood_supply, receiver_blood_supply, 'abplus_amount', quantity)
                    type = 'AB+'
                elif blood_type == 'AB-':
                    approved = request_is_approved(giver_blood_supply, receiver_blood_supply, 'abmin_amount', quantity)
                    type = 'AB-'
                elif blood_type == 'O+':
                    approved = request_is_approved(giver_blood_supply, receiver_blood_supply, 'oplus_amount', quantity)
                    type = 'O+'
                else:
                    approved = request_is_approved(giver_blood_supply, receiver_blood_supply, 'omin_amount', quantity)
                    type = 'O-'
                # ----------------------------------------------------------

                if approved:
                    messages.success(request,
                                     'A supply of blood type ' + type + ' successfully given to ' + request_o.hospital.name + "!")
                    setattr(request_o, 'status', 'Accepted')
                    request_o.save(update_fields=['status'])
                else:
                    messages.error(request, 'You do not have sufficient ' + type + ' blood in your supply.')

        elif 'D' in request.POST:
            request_o = Request.objects.get(pk=id)
            setattr(request_o, 'status', 'Declined')
            request_o.save(update_fields=['status'])

    return redirect(reverse('accounts:index'))
