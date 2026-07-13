from rest_framework import serializers

from .models import Dataset, DatasetChunk


class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetChunk
        fields = ["title", "summary", "source_ref"]


class DatasetSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="public_status", read_only=True)
    chunk_count = serializers.IntegerField(source="chunks.count", read_only=True)
    summary_items = ChunkSerializer(source="chunks", many=True, read_only=True)
    associated_agent_ids = serializers.SlugRelatedField(source="agents", slug_field="agent_id", many=True, read_only=True)
    associated_spot_ids = serializers.SlugRelatedField(source="spots", slug_field="spot_id", many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ["dataset_id", "name", "source_type", "status", "chunk_count", "summary_items", "associated_agent_ids", "associated_spot_ids", "updated_at", "failure_reason"]
