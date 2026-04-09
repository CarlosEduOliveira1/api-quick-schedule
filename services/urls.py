from django.urls import path
from . import views

urlpatterns = [
    path('service/', views.ServiceList.as_view(), name='service_list'),
    path('service/<int:pk>/', views.ServiceDetail.as_view(), name='service_detail'),

    path(
        'user/<int:user_id>/availability/',
        views.ProviderAvailabilityList.as_view(),
        name='availability_list'
    ),
    path(
        'user/<int:user_id>/availability/<int:pk>',
        views.ProviderAvailabilityDetail.as_view(),
        name='availability_detail',
    ),
]