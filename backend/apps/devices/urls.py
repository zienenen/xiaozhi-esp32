from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView


class DeviceConfigView(APIView):
    def get(self, request):
        return Response({"success": True, "data": {"module": "devices", "todo": "device config"}, "error": None})


class DeviceHeartbeatView(APIView):
    def post(self, request):
        return Response({"success": True, "data": {"module": "devices", "todo": "heartbeat accepted"}, "error": None})


urlpatterns = [
    path("device-config", DeviceConfigView.as_view(), name="device-config"),
    path("device-heartbeats", DeviceHeartbeatView.as_view(), name="device-heartbeats"),
]
