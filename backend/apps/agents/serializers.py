from rest_framework import serializers

from apps.datasets.models import Dataset
from .models import Agent


class AgentSerializer(serializers.ModelSerializer):
    dataset_id = serializers.PrimaryKeyRelatedField(source="dataset", queryset=Dataset.objects.all(), allow_null=True, required=False)
    dataset_name = serializers.CharField(source="dataset.name", read_only=True, allow_null=True)
    dataset_status = serializers.CharField(source="dataset.public_status", read_only=True, allow_null=True)
    dataset_chunk_count = serializers.IntegerField(read_only=True)
    bound_device_count = serializers.IntegerField(read_only=True)
    online_device_count = serializers.IntegerField(read_only=True)
    conversation_count = serializers.IntegerField(read_only=True)
    latest_conversation_at = serializers.DateTimeField(read_only=True, allow_null=True)
    latest_checkin_at = serializers.DateTimeField(read_only=True, allow_null=True)
    bound_devices = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = [
            "agent_id", "name", "personality_prompt", "voice_id", "knowledge_references",
            "tool_endpoint_url", "dataset_id", "status", "config_version", "prompt_version",
            "official_sync_status", "official_synced_at", "official_sync_operator",
            "official_sync_note", "official_sync_failure_reason", "series", "rarity",
            "dataset_name", "dataset_status", "dataset_chunk_count", "bound_device_count",
            "online_device_count", "conversation_count", "latest_conversation_at",
            "latest_checkin_at", "bound_devices",
        ]
        read_only_fields = [
            "config_version", "official_synced_at", "dataset_name", "dataset_status",
            "dataset_chunk_count", "bound_device_count", "online_device_count",
            "conversation_count", "latest_conversation_at", "latest_checkin_at",
            "bound_devices",
        ]

    def get_bound_devices(self, obj):
        return [
            {
                "device_id": binding.device_id,
                "sn": binding.device.sn,
                "name": binding.device.name,
                "online_status": binding.device.online_status,
                "last_seen_at": binding.device.last_seen_at,
            }
            for binding in obj.bindings.all()
        ]

    def update(self, instance, validated_data):
        configuration_fields = {
            "personality_prompt", "voice_id", "knowledge_references",
            "tool_endpoint_url", "dataset",
        }
        changed = any(
            field in validated_data and getattr(instance, field) != validated_data[field]
            for field in configuration_fields
        )
        instance = super().update(instance, validated_data)
        if changed:
            instance.config_version += 1
            instance.prompt_version = f"v{instance.config_version}"
            instance.official_sync_status = Agent.OfficialSyncStatus.NOT_SYNCED
            instance.official_synced_at = None
            instance.official_sync_failure_reason = ""
            instance.save(update_fields=[
                "config_version", "prompt_version", "official_sync_status",
                "official_synced_at", "official_sync_failure_reason",
            ])
        return instance
