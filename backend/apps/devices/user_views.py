from math import asin, cos, radians, sin, sqrt

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.agents.serializers import AgentSerializer
from apps.checkins.models import Checkin
from apps.conversations.models import ConversationSession
from apps.conversations.serializers import ConversationSessionSerializer
from apps.spots.models import ScenicSpot
from config.api import envelope
from .models import Device
from .serializers import DeviceSerializer


def current_device(request):
    devices = Device.objects.select_related("binding__agent__dataset")
    device_id = request.query_params.get("device_id")
    if device_id:
        return get_object_or_404(devices, pk=device_id)
    device = devices.filter(binding__isnull=False).order_by("-last_seen_at", "device_id").first()
    if device is None:
        raise Http404
    return device


def distance_meters(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    value = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 6371000 * 2 * asin(sqrt(value))


class UserCompanionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        device = current_device(request)
        binding = getattr(device, "binding", None)
        agent = binding.agent if binding else None
        try:
            limit = min(max(int(request.query_params.get("recent_limit", 5)), 1), 20)
        except ValueError:
            limit = 5
        sessions = (
            ConversationSession.objects.filter(device=device)
            .select_related("device", "agent", "spot")
            .prefetch_related("messages")[:limit]
        )
        return envelope({
            "device": DeviceSerializer(device).data,
            "binding": {
                "agent_id": binding.agent_id,
                "binding_type": binding.binding_type,
                "bound_at": binding.bound_at,
                "bound_by": binding.bound_by,
            } if binding else None,
            "agent": AgentSerializer(agent).data if agent else None,
            "recent_conversations": ConversationSessionSerializer(sessions, many=True).data,
        })


class UserMapView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        device = current_device(request)
        spots = list(
            ScenicSpot.objects.filter(status=ScenicSpot.Status.ACTIVE)
            .prefetch_related("nfc_tags")
            .order_by("spot_id")
        )
        real_checkins = (
            Checkin.objects.filter(
                device=device,
                source=Checkin.Source.DEVICE,
                result=Checkin.Result.SUCCESS,
            )
            .select_related("spot", "tag")
            .order_by("-checked_in_at")
        )
        latest_by_spot = {}
        for checkin in real_checkins:
            latest_by_spot.setdefault(checkin.spot_id, checkin)

        nearest_spot = None
        nearest_distance = None
        if device.last_latitude is not None and device.last_longitude is not None:
            for spot in spots:
                distance = distance_meters(
                    float(device.last_latitude),
                    float(device.last_longitude),
                    float(spot.latitude),
                    float(spot.longitude),
                )
                if nearest_distance is None or distance < nearest_distance:
                    nearest_spot, nearest_distance = spot, distance

        points = []
        for spot in spots:
            stamp = latest_by_spot.get(spot.spot_id)
            is_nearby = (
                nearest_spot is not None
                and nearest_spot.spot_id == spot.spot_id
                and nearest_distance <= spot.gps_radius_meters
            )
            active_tags = [tag for tag in spot.nfc_tags.all() if tag.status == "active"]
            points.append({
                "spot_id": spot.spot_id,
                "name": spot.name,
                "scenic_area_name": spot.scenic_area_name,
                "latitude": spot.latitude,
                "longitude": spot.longitude,
                "gps_radius_meters": spot.gps_radius_meters,
                "checkin_message": spot.checkin_message,
                "state": "stamped" if stamp else ("nearby" if is_nearby else "available"),
                "is_nearby": is_nearby,
                "distance_meters": round(nearest_distance, 1) if is_nearby else None,
                "nfc_status": "ready" if active_tags else "unavailable",
                "stamp": {
                    "checkin_id": stamp.checkin_id,
                    "checked_in_at": stamp.checked_in_at,
                    "tag_id": stamp.tag_id,
                    "source": stamp.source,
                } if stamp else None,
            })

        latest_nfc = real_checkins.first()
        return envelope({
            "device_id": device.device_id,
            "location": {
                "gps_status": device.last_gps_status,
                "latitude": device.last_latitude,
                "longitude": device.last_longitude,
                "quality": device.last_location_quality,
                "updated_at": device.last_location_at,
                "nearest_spot_id": nearest_spot.spot_id if nearest_spot else None,
                "nearest_distance_meters": round(nearest_distance, 1) if nearest_distance is not None else None,
                "is_near_spot": bool(
                    nearest_spot and nearest_distance <= nearest_spot.gps_radius_meters
                ),
            },
            "nfc": {
                "status": latest_nfc.tag.status if latest_nfc and latest_nfc.tag else "not_seen",
                "tag_id": latest_nfc.tag_id if latest_nfc else None,
                "spot_id": latest_nfc.spot_id if latest_nfc else None,
                "last_seen_at": latest_nfc.checked_in_at if latest_nfc else None,
            },
            "stamp_summary": {
                "earned": len(latest_by_spot),
                "total": len(spots),
                "simulation_excluded": True,
            },
            "points": points,
        })
