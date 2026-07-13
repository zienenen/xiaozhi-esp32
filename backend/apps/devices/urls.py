from django.urls import path
from .views import BindingEventsView, BindingView, DeviceConfigView, DeviceDetailView, DeviceHeartbeatView, DeviceListView

urlpatterns = [
    path("device-config", DeviceConfigView.as_view()),
    path("device-heartbeats", DeviceHeartbeatView.as_view()),
    path("devices", DeviceListView.as_view()),
    path("devices/<str:device_id>", DeviceDetailView.as_view()),
    path("bindings", BindingView.as_view()),
    path("binding-events", BindingEventsView.as_view()),
]
