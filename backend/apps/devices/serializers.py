from rest_framework import serializers

from .models import BindingEvent, Device, DeviceBinding


class DeviceSerializer(serializers.ModelSerializer):
    bound_agent_id = serializers.CharField(source="binding.agent_id", read_only=True, allow_null=True)

    class Meta:
        model = Device
        fields = ["device_id", "sn", "name", "device_token_ref", "online_status", "bound_agent_id", "last_seen_at", "last_gps_status", "firmware_version", "battery_percent", "last_latitude", "last_longitude", "last_location_quality", "last_location_at"]
        read_only_fields = [f for f in fields if f != "name"]


class BindingSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source="device.device_id", read_only=True)
    agent_id = serializers.CharField(source="agent.agent_id", read_only=True)

    class Meta:
        model = DeviceBinding
        fields = ["device_id", "agent_id", "bound_by", "bound_at", "binding_type", "reason"]


class BindingEventSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source="device.device_id")
    agent_id = serializers.CharField(source="agent.agent_id")

    class Meta:
        model = BindingEvent
        fields = ["device_id", "agent_id", "bound_by", "bound_at", "binding_type", "reason"]
