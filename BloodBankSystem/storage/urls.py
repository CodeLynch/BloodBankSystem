from django.urls import path, include
from . import views

app_name = 'storage'

urlpatterns = [
    path('create_blood_supply/', views.CreateBloodSupplyView.as_view(), name='create_blood_supply'),
    path('update_blood_supply/', views.UpdateBloodSupplyView.as_view(), name='update_blood_supply'),
    path('delete_blood_supply/', views.DeleteBloodSupplyView.as_view(), name='delete_blood_supply'),
    path('update_donation/<int:id>/', views.update_donation, name="update_donation"),
    path('update_request/<int:id>', views.update_request, name='update_request'),
]