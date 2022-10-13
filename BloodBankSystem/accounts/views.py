from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.models import *
from accounts.forms import *


class HomeView(View):
    template = 'index.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            requests = ''
            user = User.objects.get(username=request.session['username'])
            if request.session['type'] == 'R':
                lists = Transfusion.objects.filter(recipient=user.user_id).order_by('-transfusion_date')
            elif request.session['type'] == 'H':
                lists = Transfusion.objects.filter(hospital=user.user_id, status='pending').order_by('-transfusion_date')
                requests = Request.objects.filter(hospital=user.user_id, status='pending').order_by('-request_date')
            elif request.session['type'] == 'D':
                lists = Donation.objects.filter(donor=user.user_id).order_by('-donation_date')
            elif request.session['type'] == 'B':
                lists = Donation.objects.filter(blood_bank=user.user_id, status="pending").order_by('-donation_date')
                requests = Request.objects.filter(blood_bank=user.user_id, status="pending").order_by('-request_date')
                
            lists_paginator = Paginator(lists, 5)
            lists_page_number = request.GET.get('lists_page')
            lists = lists_paginator.get_page(lists_page_number)
            
            requests_paginator = Paginator(requests, 5)
            requests_page_number = request.GET.get('requests_page')
            requests = requests_paginator.get_page(requests_page_number)

            context = {'lists': lists, 'requests': requests, 'user_image': user.image_tag}
            return render(request, self.template, context)


class LoginView(View):
    template = 'login.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            if User.objects.get(username=username):
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session['username'] = user.username
                    if user.type == 'I':
                        individual = Individual.objects.get(username=user.username)
                        request.session['first_name'] = individual.first_name
                        request.session['last_name'] = individual.last_name
                        request.session['type'] = individual.individual_type
                        request.session['blood_type'] = individual.blood_type
                    elif user.type == 'O':
                        org = Organization.objects.get(username=user.username)
                        request.session['name'] = org.name
                        request.session['type'] = org.org_type
                        request.session['blood_supply_id'] = org.blood_supply_id
                    return redirect(reverse('accounts:index'))
                messages.error(request, 'Password is incorrect.')
        except User.DoesNotExist:
            user = None
            messages.error(request, 'No such username exist.')
        return render(request, self.template)


class LogoutView(View):

    def get(self, request):
        request.session.flush()
        messages.success(request, 'User was logged out successfully.')
        return redirect(reverse('accounts:login'))


def registration_view(request, type = None):
    template = 'register.html'

    if type == 'donor':
        form = DonorForm()
        user_type = 'Donor'
    elif type == 'recipient':
        form = RecipientForm()
        user_type = 'Recipient'
    elif type == 'hospital':
        form = HospitalForm()
        user_type = 'Hospital'
    elif type == 'blood_bank':
        form = BloodBankForm()
        user_type = 'Blood bank'

    if request.method == 'POST':
        if type == 'donor':
            form = DonorForm(request.POST, request.FILES)
            user_type = 'Donor'
        elif type == 'recipient':
            form = RecipientForm(request.POST, request.FILES)
            user_type = 'Recipient'
        elif type == 'hospital':
            form = HospitalForm(request.POST, request.FILES)
            user_type = 'Hospital'
        elif type == 'blood_bank':
            form = BloodBankForm(request.POST, request.FILES)
            user_type = 'Blood bank'
        if form.is_valid():
            form.save()
            messages.success(request, user_type + ' registered successfully!')
            return redirect(reverse('accounts:login'))
    
    context = {'form': form, 'user_type': user_type}
    return render(request, template, context)


class EditProfileView(View):
    template = 'edit_profile.html'

    def get(self, request):
        user = User.objects.get(username=request.session['username'])
        if user.type == 'I':
            individual = Individual.objects.get(username=user.username)
            if individual.individual_type == 'R':
                form = RecipientForm(instance=individual)
            else:
                form = DonorForm(instance=individual)
        elif user.type == 'O':
            org = Organization.objects.get(username=user.username)
            if org.org_type == 'H':
                form = HospitalForm(instance=org)
            else:
                form = BloodBankForm(instance=org)
        return render(request, self.template, {'form': form, 'user_image': user.image_tag})

    def post(self, request):
        user = User.objects.get(username=request.session['username'])
        if user.type == 'I':
            individual = Individual.objects.get(username=user.username)
            if individual.individual_type == 'R':
                form = RecipientForm(request.POST, request.FILES, instance=individual)
            else:
                form = DonorForm(request.POST, request.FILES, instance=individual)
        elif user.type == 'O':
            org = Organization.objects.get(username=user.username)
            if org.org_type == 'H':
                form = HospitalForm(request.POST, request.FILES, instance=org)
            else:
                form = BloodBankForm(request.POST, request.FILES, instance=org)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            form.save()

            if 'remove_user_image' in request.POST:
                user.set_to_default()
                user.save()

            messages.success(request, 'Profile updated successfully!')
            try:
                if User.objects.get(username=username):
                    user = User.objects.get(username=username)
                    if user.password == password:
                        request.session['username'] = user.username
                        if user.type == 'I':
                            individual = Individual.objects.get(username=user.username)
                            request.session['first_name'] = individual.first_name
                            request.session['last_name'] = individual.last_name
                        elif user.type == 'O':
                            org = Organization.objects.get(username=user.username)
                            request.session['name'] = org.name
            except User.DoesNotExist:
                user = None
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})
