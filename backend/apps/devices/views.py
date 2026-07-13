from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.agents.models import Agent
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot
from config.api import api_error, envelope
from .authentication import authenticate_device
from .models import BindingEvent, Device, DeviceBinding
from .serializers import BindingEventSerializer, BindingSerializer, DeviceSerializer


class DeviceConfigView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        device, error = authenticate_device(request)
        if error:
            return error
        try:
            agent = device.binding.agent
        except DeviceBinding.DoesNotExist:
            return api_error("device_not_bound", "设备未绑定角色")
        spots = ScenicSpot.objects.filter(status=ScenicSpot.Status.ACTIVE)
        tags = NfcTag.objects.filter(status=NfcTag.Status.ACTIVE, spot__in=spots)
        if not agent.dataset_id or not spots.exists() or not tags.exists():
            return api_error("config_not_ready", "设备配置尚未就绪")
        return envelope({
            "device_id": device.device_id,
            "agent": {"agent_id": agent.agent_id, "name": agent.name, "voice_id": agent.voice_id, "personality_prompt": agent.personality_prompt, "dataset_id": agent.dataset_id},
            "spots": [{"spot_id": spot.spot_id, "name": spot.name, "latitude": float(spot.latitude), "longitude": float(spot.longitude), "gps_radius_meters": spot.gps_radius_meters, "dataset_id": spot.dataset_id} for spot in spots],
            "nfc_tags": [{"tag_id": tag.tag_id, "spot_id": tag.spot_id, "status": tag.status} for tag in tags],
        })


class DeviceHeartbeatView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        device, error = authenticate_device(request, request.data.get("device_id"))
        if error:
            return error
        if request.data.get("device_id") != device.device_id:
            return api_error("device_id_mismatch", "设备编号不一致")
        device.online_status = Device.Status.ONLINE
        device.last_seen_at = timezone.now()
        device.firmware_version = request.data.get("firmware_version", "")
        device.battery_percent = request.data.get("battery_percent")
        device.last_gps_status = request.data.get("gps_status", "")
        device.save(update_fields=["online_status", "last_seen_at", "firmware_version", "battery_percent", "last_gps_status"])
        return envelope({"accepted": True, "last_seen_at": device.last_seen_at})


class DeviceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return envelope(DeviceSerializer(Device.objects.select_related("binding__agent"), many=True).data)


class DeviceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, device_id):
        return envelope(DeviceSerializer(get_object_or_404(Device, pk=device_id)).data)

    def patch(self, request, device_id):
        serializer = DeviceSerializer(get_object_or_404(Device, pk=device_id), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return envelope(serializer.data)


class BindingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = DeviceBinding.objects.select_related("device", "agent")
        if request.query_params.get("device_id"):
            rows = rows.filter(device_id=request.query_params["device_id"])
        return envelope(BindingSerializer(rows, many=True).data)

    def post(self, request):
        device = get_object_or_404(Device, pk=request.data.get("device_id"))
        agent = get_object_or_404(Agent, pk=request.data.get("agent_id"))
        values = {"agent": agent, "binding_type": request.data.get("binding_type", DeviceBinding.Type.ADMIN_OVERRIDE), "reason": request.data.get("reason", ""), "bound_by": request.user.username}
        binding, _ = DeviceBinding.objects.update_or_create(device=device, defaults=values)
        BindingEvent.objects.create(device=device, **values)
        return envelope(BindingSerializer(binding).data)


class BindingEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return envelope(BindingEventSerializer(BindingEvent.objects.select_related("device", "agent"), many=True).data)
