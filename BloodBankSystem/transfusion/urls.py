from django.urls import path
from . import views

app_name = 'transfusion'

urlpatterns = [
    path('', views.TransfusionView.as_view(), name='index'),
    path('update_transfusion/<int:id>', views.update_transfusion, name='update_transfusion'),
]