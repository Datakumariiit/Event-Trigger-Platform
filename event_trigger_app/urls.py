from django.urls import path, include
from .views import create_trigger, trigger_event, view_triggers, edit_trigger, delete_trigger 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Event Trigger API",
        default_version='v1',
        description="API documentation for the Event Trigger application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('create_trigger/', create_trigger, name='create_trigger'),
    path('trigger_event/<int:trigger_id>/', trigger_event, name='trigger_event'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('triggers/', view_triggers, name='view_triggers'),
    path('trigger/edit/<int:trigger_id>/', edit_trigger, name='edit_trigger'),
    path('trigger/delete/<int:trigger_id>/', delete_trigger, name='delete_trigger'),
]
