from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from accounts.models import Recipient, Hospital
from transfusion.forms import TransfusionForm

# Create your views here.

class TransfusionView(View):
    template = 'transfusion_index.html'

    def get(self, request):
        form = TransfusionForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = TransfusionForm(request.POST)
        user_id = request.POST['hospital'].split(":")[0]
        if form.is_valid():
            hospital = Hospital.objects.get(user_id=user_id)
            transfusion = form.save(commit=False)
            transfusion.hospital = hospital
            transfusion.status = True
            recipient = Recipient.objects.get(username=request.session['username'])
            transfusion.recipient = recipient
            transfusion.save()
        return redirect(reverse('accounts:index'))

