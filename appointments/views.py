from django.shortcuts import render
from django.db import models
from rest_framework import generics, permissions

from .models import Scheduling
from .serializers import SchedulingSerializer

# Create your views here.
class AppointmentsList(generics.ListCreateAPIView):
    serializer_class = SchedulingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Scheduling.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)