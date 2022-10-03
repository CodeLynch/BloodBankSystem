from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register_<str:type>/', views.RegistrationView, name='register'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
]