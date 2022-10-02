from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from request.forms import *

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
        user_id = request.POST['hospital'].split(":")[0]
        if form.is_valid():
            hospital= Hospital.objects.get(user_id=user_id)
            requestt = form.save(commit=False)
            requestt.hospital = hospital
            requestt.status = True
            requestt.save()
            messages.success(request, 'Blood supply requested successfully!')
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})