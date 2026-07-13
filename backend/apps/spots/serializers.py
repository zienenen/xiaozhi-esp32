from rest_framework import serializers

from apps.datasets.models import Dataset
from .models import ScenicSpot


class ScenicSpotSerializer(serializers.ModelSerializer):
    dataset_id = serializers.PrimaryKeyRelatedField(source="dataset", queryset=Dataset.objects.all(), allow_null=True, required=False)

    class Meta:
        model = ScenicSpot
        fields = ["spot_id", "name", "scenic_area_name", "latitude", "longitude", "gps_radius_meters", "dataset_id", "checkin_message", "status"]
