from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Individual)
admin.site.register(Organization)
admin.site.register(Donor)
admin.site.register(Recipient)
admin.site.register(Hospital)
admin.site.register(BloodBank)
admin.site.register(BloodSupply)
admin.site.register(Transfusion)
admin.site.register(Donation)
admin.site.register(Request)
