from django.shortcuts import render
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

    def perform_create(self, serializer):
        self.permission_classes = [IsAuthenticated]
        user = self.request.user

        if user.user_type != 'P':
            raise PermissionDenied('Only provider can create services')
        serializer.save(provider=user)

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]