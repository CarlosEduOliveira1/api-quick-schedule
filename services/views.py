from django.shortcuts import render
from django.db import models
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .models import Service
from .serializers import ServiceSerializer
from .permissions import IsOwnerOrReadOnly

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