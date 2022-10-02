from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from .forms import *

# Create your views here.


class RequestBloodSupplyView(View):
    template = 'request_blood_supply.html'

    def get(self, request):
        form = RequestBloodSupplyForm
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = RequestBloodSupplyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood supply requested successfully!')
            return redirect(reverse('accounts:index'))
        return render(request, self.template, {'form': form})