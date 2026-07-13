from math import asin, cos, radians, sin, sqrt

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.checkins.models import Checkin
from apps.checkins.serializers import CheckinSerializer
from apps.checkins.services import COOLDOWN_SECONDS, create_checkin
from apps.datasets.models import Dataset
from apps.datasets.serializers import DatasetSerializer
from apps.devices.models import Device
from apps.devices.serializers import DeviceSerializer
from apps.spots.models import ScenicSpot
from config.api import api_error, envelope


class DemoOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        devices = Device.objects.select_related("binding__agent")
        latest = Checkin.objects.select_related("device", "agent", "spot", "tag")[:20]
        device = devices.first()
        latest_checkin = latest.first()
        agent = getattr(getattr(device, "binding", None), "agent", None) if device else None
        dataset = agent.dataset if agent else None
        near_spot = None
        if device and device.last_latitude is not None and device.last_longitude is not None:
            near_spot = next((spot for spot in ScenicSpot.objects.filter(status=ScenicSpot.Status.ACTIVE)
                              if _distance_meters(float(device.last_latitude), float(device.last_longitude), float(spot.latitude), float(spot.longitude)) <= spot.gps_radius_meters), None)
        latest_data = CheckinSerializer(latest_checkin).data if latest_checkin else None
        if latest_data:
            latest_data["spot_name"] = latest_checkin.spot.name
            latest_data["agent_name"] = latest_checkin.agent.name
        return envelope({
            "devices": DeviceSerializer(devices, many=True).data,
            "checkins": CheckinSerializer(latest, many=True).data,
            "datasets": DatasetSerializer(Dataset.objects.prefetch_related("chunks", "agents", "spots"), many=True).data,
            "summary": {"device_count": devices.count(), "online_count": devices.filter(online_status="online").count(), "spot_count": ScenicSpot.objects.count(), "checkin_count": Checkin.objects.count()},
            "device": DeviceSerializer(device).data if device else None,
            "agent": AgentSerializer(agent).data if agent else None,
            "gps": ({"status": device.last_gps_status, "fix": device.last_gps_status == "fixed", "near_spot": near_spot is not None,
                     "updated_at": device.last_location_at} if device else None),
            "nfc": ({"status": latest_checkin.tag.status, "tag_id": latest_checkin.tag_id, "spot_id": latest_checkin.spot_id}
                    if latest_checkin and latest_checkin.tag else None),
            "latest_checkin": latest_data,
            "dataset": DatasetSerializer(dataset).data if dataset else None,
            "events": ([{"time": latest_checkin.checked_in_at, "message": f"{latest_checkin.spot.name}打卡：{latest_checkin.result}"}]
                       if latest_checkin else []),
        })


def _distance_meters(lat1, lon1, lat2, lon2):
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    value = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 6371000 * 2 * asin(sqrt(value))


class SimulateCheckinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not (request.user.is_staff or request.user.groups.filter(name__in=["factory_admin", "tester"]).exists()):
            return api_error("permission_denied", "仅测试或原厂账号可执行模拟打卡", status=403)
        device = get_object_or_404(Device, pk=request.data.get("device_id"))
        checkin, code = create_checkin(device=device, spot_id=request.data.get("spot_id"), tag_id=request.data.get("tag_id"), source=Checkin.Source.SIMULATION)
        if code == "duplicate":
            return envelope({"accepted": False, "result": "duplicate", "last_checkin_id": checkin.checkin_id, "cooldown_seconds": COOLDOWN_SECONDS, "source": "simulation"})
        if code:
            return api_error(code, "模拟打卡校验失败")
        return envelope({"accepted": True, "result": "simulated", "checkin_id": checkin.checkin_id, "source": "simulation"})
from apps.agents.serializers import AgentSerializer
