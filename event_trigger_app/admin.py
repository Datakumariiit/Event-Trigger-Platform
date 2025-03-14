from django.contrib import admin
from .models import Trigger, EventLog

@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('name', 'trigger_type', 'schedule_time', 'interval', 'is_active')

@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('trigger', 'triggered_at', 'is_manual_test', 'archived')
