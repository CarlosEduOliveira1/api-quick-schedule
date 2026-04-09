from rest_framework import serializers
from .models import Service, ProviderAvailability

class ServiceSerializer(serializers.ModelSerializer):
    provider = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'provider',
            'name',
            'description',
            'price',
            'duration',
            'is_active',
        ]

class ProviderAvailabilitySerializer(serializers.ModelSerializer):
    provider = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    hour_beginning = serializers.TimeField(format="%H:%M")
    hour_ending = serializers.TimeField(format="%H:%M")

    week_day_display = serializers.CharField(
        source='get_week_day_display',
        read_only=True
    )

    class Meta:
        model = ProviderAvailability
        fields = [
            'id',
            'provider',
            'week_day',
            'week_day_display',
            'hour_beginning',
            'hour_ending',
        ]
    def validate(self, data):
        if data['hour_ending'] <= data['hour_beginning']:
            raise serializers.ValidationError(
                'hour_beggining must be before hour_ending'
            )
        return data