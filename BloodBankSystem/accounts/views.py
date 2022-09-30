from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views import View
from.models import User, Individual, Organization, Donor, Recipient, Hospital, BloodBank
from .forms import DonorForm, RecipientForm, HospitalForm, BloodBankForm

class HomeView(View):
    template = 'index.html'

    def get(self, request):
        if 'username' not in request.session:
            return redirect(reverse('accounts:login'))
        else:
            return render(request, self.template)


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
                    elif user.type == 'O':
                        org = Organization.objects.get(username=user.username)
                        request.session['name'] = org.name
                        request.session['type'] = org.org_type
                    return redirect(reverse('accounts:index'))
        except User.DoesNotExist:
            user = None
        return render(request, self.template)


class LogoutView(View):

    def get(self, request):
        request.session.clear()
        return redirect(reverse('accounts:login'))


class DonorRegistrationView(View):
    template = 'register.html'

    def get(self, request):
        form = DonorForm()
        context = {'form': form}
        return render(request, self.template, context)
    
    def post(self, request):
        form = DonorForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login'))
        return render(request, self.template, context)


class RecipientRegistrationView(View):
    template = 'register.html'

    def get(self, request):
        form = RecipientForm()
        context = {'form': form}
        return render(request, self.template, context)
    
    def post(self, request):
        form = RecipientForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login'))
        return render(request, self.template, context)


class HospitalRegistrationView(View):
    template = 'register.html'

    def get(self, request):
        form = HospitalForm()
        context = {'form': form}
        return render(request, self.template, context)
    
    def post(self, request):
        form = HospitalForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login'))
        return render(request, self.template, context)


class BloodBankRegistrationView(View):
    template = 'register.html'

    def get(self, request):
        form = BloodBankForm()
        context = {'form': form}
        return render(request, self.template, context)
    
    def post(self, request):
        form = BloodBankForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login'))
        return render(request, self.template, context)


class EditRecipientView(View):
    template = 'edit_recipient.html'

    def get(self, request):
        recipient = Recipient.objects.get(username=request.session['username'])
        form = RecipientForm(instance=recipient)
        return render(request, self.template, {'form': form})

    def post(self, request):
        recipient = Recipient.objects.get(username=request.session['username'])
        form = RecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            form.save()
            # print(username)
            try:
                if Recipient.objects.get(username=username):
                    recipient = Recipient.objects.get(username=username)
                    if recipient.password == password:
                        request.session['username'] = recipient.username
                        request.session['first_name'] = recipient.first_name
                        request.session['last_name'] = recipient.last_name
            except User.DoesNotExist:
                user = None
        return redirect(reverse('accounts:index'))