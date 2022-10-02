from django.urls import path, include
from . import views

app_name = 'request'

urlpatterns = [
    path('request_blood_supply/', views.RequestBloodSupplyView.as_view(), name='request_blood_supply'),
]