from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.devices.authentication import authenticate_device
from apps.devices.models import Device
from apps.spots.models import ScenicSpot
from config.api import api_error, envelope
from .models import Checkin
from .serializers import CheckinSerializer
from .services import COOLDOWN_SECONDS, create_checkin


class LocationEventsView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        device, error = authenticate_device(request, request.data.get("device_id"))
        if error:
            return error
        if request.data.get("device_id") != device.device_id:
            return api_error("device_id_mismatch", "设备编号不一致")
        if request.data.get("spot_id") and not ScenicSpot.objects.filter(pk=request.data["spot_id"]).exists():
            return api_error("spot_not_found", "点位不存在", status=404)
        device.last_latitude = request.data.get("latitude")
        device.last_longitude = request.data.get("longitude")
        device.last_location_quality = request.data.get("location_quality") or {}
        device.last_location_at = parse_datetime(request.data.get("event_time", "")) or __import__("django.utils.timezone", fromlist=["now"]).now()
        device.last_gps_status = "fixed" if device.last_location_quality.get("fix") else "no_fix"
        device.save(update_fields=["last_latitude", "last_longitude", "last_location_quality", "last_location_at", "last_gps_status"])
        return envelope({"accepted": True, "event_type": request.data.get("event_type"), "checkin_created": False})


class CheckinListView(APIView):
    def get_permissions(self):
        return [] if self.request.method == "POST" else [IsAuthenticated()]

    def get(self, request):
        rows = Checkin.objects.select_related("device", "agent", "spot", "tag")
        for key in ("device_id", "spot_id", "result", "source"):
            if request.query_params.get(key):
                rows = rows.filter(**{key: request.query_params[key]})
        if request.query_params.get("date_from"):
            rows = rows.filter(checked_in_at__gte=request.query_params["date_from"])
        if request.query_params.get("date_to"):
            rows = rows.filter(checked_in_at__lte=request.query_params["date_to"])
        return envelope(CheckinSerializer(rows, many=True).data)

    def post(self, request):
        device, error = authenticate_device(request, request.data.get("device_id"))
        if error:
            return error
        if request.data.get("source", "device") != "device":
            return api_error("invalid_source", "设备接口只能创建真实设备记录")
        event_time = parse_datetime(request.data.get("event_time", ""))
        checkin, code = create_checkin(device=device, spot_id=request.data.get("spot_id"), tag_id=request.data.get("tag_id"), source=Checkin.Source.DEVICE, event_time=event_time, location_quality=request.data.get("location_quality"))
        if code == "duplicate":
            return envelope({"accepted": False, "result": "duplicate", "last_checkin_id": checkin.checkin_id, "cooldown_seconds": COOLDOWN_SECONDS})
        if code:
            return api_error(code, "打卡校验失败")
        return envelope({"accepted": True, "result": "success", "checkin_id": checkin.checkin_id, "agent_id": checkin.agent_id, "spot_id": checkin.spot_id, "speak_text": checkin.spot.checkin_message, "next_action": "start_spot_qa"})


class CheckinDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, checkin_id):
        return envelope(CheckinSerializer(get_object_or_404(Checkin, pk=checkin_id)).data)
