from django.shortcuts import render, get_object_or_404
from django.db import models
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from users.models import User
from .models import Service, ProviderAvailability
from .serializers import ServiceSerializer, ProviderAvailabilitySerializer
from .permissions import IsProvider, IsOwnerOrReadOnly

# Create your views here.
class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    queryset = queryset.filter(is_active=True)

    def perform_create(self, serializer):
        self.permission_classes = [IsAuthenticated]
        user = self.request.user

        if user.user_type != 'P':
            raise PermissionDenied('Only provider can create services')
        serializer.save(provider=user)

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Service.objects.filter(
                models.Q(is_active=True) | models.Q(provider=user)
            )

        return Service.objects.filter(is_active=True)
    
class ProviderAvailabilityList(generics.ListCreateAPIView):
    serializer_class = ProviderAvailabilitySerializer

    def get_provider(self):
        return get_object_or_404(
            User,
            pk=self.kwargs['user_id'],
            user_type='P'
        )
    
    def get_queryset(self):
        return ProviderAvailability.objects.filter(
            provider=self.get_provider()
        )

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsProvider()]
    
    def perform_create(self, serializer):
        provider = self.get_provider()
        if provider !=  self.request.user:
            raise PermissionDenied('You can not create Provider Availabilities')
        serializer.save(provider=provider)

class ProviderAvailabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProviderAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        provider = get_object_or_404(
            User,
            pk=self.kwargs['user_id'],
            user_type='P'
        )
        return ProviderAvailability.objects.filter(provider=provider)