from rest_framework import serializers

from .models import Checkin


class CheckinSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source="device.device_id")
    agent_id = serializers.CharField(source="agent.agent_id")
    spot_id = serializers.CharField(source="spot.spot_id")
    tag_id = serializers.CharField(source="tag.tag_id", allow_null=True)

    class Meta:
        model = Checkin
        fields = ["checkin_id", "device_id", "agent_id", "spot_id", "tag_id", "result", "failure_code", "source", "checked_in_at", "location_quality", "latitude", "longitude"]
