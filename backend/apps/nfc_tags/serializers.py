from rest_framework import serializers

from apps.spots.models import ScenicSpot
from .models import NfcTag


class NfcTagSerializer(serializers.ModelSerializer):
    spot_id = serializers.PrimaryKeyRelatedField(source="spot", queryset=ScenicSpot.objects.all())

    class Meta:
        model = NfcTag
        fields = ["tag_id", "spot_id", "label", "status", "last_seen_at"]
        read_only_fields = ["last_seen_at"]
