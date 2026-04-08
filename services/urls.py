from django.urls import path
from . import views

urlpatterns = [
    path('service/', views.ServiceList.as_view(), name='service_list'),
    path('service/<int:pk>/', views.ServiceDetail.as_view(), name='service_detail'),
]