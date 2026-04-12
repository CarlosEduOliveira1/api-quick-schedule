from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.AppointmentsList.as_view(), name='appointments_list'),
    path('appointments/<int:pk>/', views.AppointmentsDetail.as_view(), name='appointment_detail'),
    path('appointments/<int:pk>/confirm/', views.confirm_appointments, name='appointment_confirm'),
]