from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register_donor/', views.DonorRegistrationView.as_view(), name='register_donor'),
    path('register_recipient/', views.RecipientRegistrationView.as_view(), name='register_recipient'),
    path('register_hospital/', views.HospitalRegistrationView.as_view(), name='register_hospital'),
    path('register_blood_bank/', views.BloodBankRegistrationView.as_view(), name='register_blood_bank'),
    path('edit_recipient/', views.EditRecipientView.as_view(), name='edit_recipient'),
]