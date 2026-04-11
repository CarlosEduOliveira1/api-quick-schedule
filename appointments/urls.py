from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.AppointmentsList.as_view(), name='appointments_list'),
]