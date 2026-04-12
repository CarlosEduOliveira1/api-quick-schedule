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
        service = data.get(
            'service', 
            self.instance.service if self.instance else None
        )
        beginning = data.get(
            'hour_beginning',
            self.instance.hour_beginning if self.instance else None
        )
        
        if not service or not beginning:
            return data

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
        )

        if self.instance:
            conflicting_schedule = conflicting_schedule.exclude(pk=self.instance.pk)

        if conflicting_schedule.exists():
            raise serializers.ValidationError('The provider already has an appointment.')
        
        return data
        