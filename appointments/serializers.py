from rest_framework import serializers
from django.utils import timezone
from .models import Scheduling

class SchedulingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduling
        fields = ['id','service','hour_beginning','hour_ending','status','created_at']
        read_only_fields = ['hour_ending', 'status', 'created_at']

    def validate_hour_beginning(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Can not schedule in the past')
        return value
    
    def validate(self, data):
        service = data['service']
        beginning = data['hour_beginning']

        # from datetime import timedelta
        # ending = beginning + timedelta(minutes=service.duration)
        ending = beginning + service.duration

        week_day = beginning.weekday()
        available = service.provider.provideravailability_set.filter(
            week_day=week_day,
            hour_beginning__lte=beginning.time(),
            hour_ending__gte=ending.time(),
        ).exists()

        if not available:
            raise serializers.ValidationError('The provider is not available during this day/time.')
        
        conflicting_schedule = Scheduling.objects.filter(
            service__provider=service.provider,
            status__in=['pending', 'confirmed'],
            hour_beginning__lt=ending,
            hour_ending__gt=beginning,
        ).exists()

        if conflicting_schedule:
            raise serializers.ValidationError('The provider already has an appointment.')
        
        return data
        