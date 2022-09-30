from django.urls import path
from . import views
app_name = 'transfusion'

urlpatterns = [
    path('', views.TransfusionView.as_view(), name='index'),
]