from django.shortcuts import render
from django.db import models
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

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

class AppointmentsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchedulingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Scheduling.objects.filter(customer=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        scheduling = self.get_object()
        scheduling.status = 'canceled'
        scheduling.save()
        return Response({'detail': 'Appointment is canceled successfully.'}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def confirm_appointments(request, pk):
    try:
        scheduling = Scheduling.objects.get(pk=pk)
    except Scheduling.DoesNotExist:
        return Response({'detail': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != scheduling.service.provider:
        return Response({'detail': 'Only the provider can cancel the appointment'}, status=status.HTTP_403_FORBIDDEN)
    
    if scheduling.status != 'pending':
        return Response(
            {'detail': f'Appointment can not be confirmed because the status is {scheduling.status}'},
            status=status.HTTP_400_BAD_REQUEST
            )
    
    scheduling.status = 'confirmed'
    scheduling.save()

    return Response({'detail': 'Appointment confirmed successfully'}, status=status.HTTP_200_OK)