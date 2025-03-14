from django.db import models

class Trigger(models.Model):
    TRIGGER_TYPE_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('api', 'API')
    ]

    name = models.CharField(max_length=100)
    trigger_type = models.CharField(max_length=10, choices=TRIGGER_TYPE_CHOICES)
    schedule_time = models.DateTimeField(null=True, blank=True)
    interval = models.PositiveIntegerField(null=True, blank=True)  # in minutes
    api_payload = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class EventLog(models.Model):
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE)
    triggered_at = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField(null=True, blank=True)
    is_manual_test = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
