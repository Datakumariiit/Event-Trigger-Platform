from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
import json
from .models import Trigger, EventLog

@swagger_auto_schema(
    method='POST',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'trigger_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['scheduled', 'api']),
            'schedule_time': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
            'interval': openapi.Schema(type=openapi.TYPE_INTEGER),
            'api_payload': openapi.Schema(type=openapi.TYPE_OBJECT)
        }
    )
)
@api_view(['POST'])
@csrf_exempt
def create_trigger(request):
    data = json.loads(request.body)
    trigger = Trigger.objects.create(
        name=data['name'],
        trigger_type=data['trigger_type'],
        schedule_time=data.get('schedule_time'),
        interval=data.get('interval'),
        api_payload=data.get('api_payload'),
    )
    return JsonResponse({"message": "Trigger created successfully", "trigger_id": trigger.id})

@swagger_auto_schema(
    method='POST', 
    responses={200: "Event triggered successfully", 404: "Trigger not found"}
)
@api_view(['POST'])
@csrf_exempt
def trigger_event(request, trigger_id):
    try:
        trigger = Trigger.objects.get(id=trigger_id)
        payload = trigger.api_payload if trigger.trigger_type == 'api' else None
        log_event(trigger, payload)
        return JsonResponse({"message": "Event triggered successfully"})
    except Trigger.DoesNotExist:
        return JsonResponse({"error": "Trigger not found"}, status=404)

def log_event(trigger, payload=None, is_manual_test=False):
    EventLog.objects.create(
        trigger=trigger,
        payload=payload,
        is_manual_test=is_manual_test
    )

@api_view(['GET'])
def view_triggers(request):
    triggers = Trigger.objects.all().values()
    return JsonResponse(list(triggers), safe=False)

@swagger_auto_schema(
    method='PUT',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'trigger_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['scheduled', 'api']),
            'schedule_time': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
            'interval': openapi.Schema(type=openapi.TYPE_INTEGER),
            'api_payload': openapi.Schema(type=openapi.TYPE_OBJECT)
        }
    )
)
@api_view(['PUT'])
@csrf_exempt
def edit_trigger(request, trigger_id):
    try:
        trigger = Trigger.objects.get(id=trigger_id)
        data = json.loads(request.body)
        
        trigger.name = data.get('name', trigger.name)
        trigger.trigger_type = data.get('trigger_type', trigger.trigger_type)
        trigger.schedule_time = data.get('schedule_time', trigger.schedule_time)
        trigger.interval = data.get('interval', trigger.interval)
        trigger.api_payload = data.get('api_payload', trigger.api_payload)

        trigger.save()
        return JsonResponse({"message": "Trigger updated successfully"})
    except Trigger.DoesNotExist:
        return JsonResponse({"error": "Trigger not found"}, status=404)

@api_view(['DELETE'])
@csrf_exempt
def delete_trigger(request, trigger_id):
    try:
        trigger = Trigger.objects.get(id=trigger_id)
        trigger.delete()
        return JsonResponse({"message": "Trigger deleted successfully"})
    except Trigger.DoesNotExist:
        return JsonResponse({"error": "Trigger not found"}, status=404)