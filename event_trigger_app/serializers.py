from rest_framework import serializers
from .models import Trigger, EventLog

class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        fields = '__all__'

class EventLogSerializer(serializers.ModelSerializer):
    trigger = TriggerSerializer(read_only=True)  # Nested serializer to show trigger details
    
    class Meta:
        model = EventLog
        fields = '__all__'
