from django.utils import timezone
from rest_framework import serializers

from apps.agents.models import Agent
from apps.devices.models import Device
from apps.spots.models import ScenicSpot
from .models import ConversationMessage, ConversationSession, OfficialSyncLog


SENSITIVE_KEYS = (
    "token", "password", "secret", "authorization", "credential",
    "api_key", "access_key", "private_key", "cookie",
)


def sanitize_snapshot(value):
    if isinstance(value, dict):
        return {
            key: ("***" if any(marker in key.lower() for marker in SENSITIVE_KEYS) else sanitize_snapshot(item))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [sanitize_snapshot(item) for item in value]
    return value


class ConversationMessageSerializer(serializers.ModelSerializer):
    session_id = serializers.PrimaryKeyRelatedField(
        source="session", queryset=ConversationSession.objects.all(), required=False
    )

    class Meta:
        model = ConversationMessage
        fields = ["message_id", "session_id", "role", "content", "content_source", "created_at", "metadata"]
        read_only_fields = ["message_id"]


class ConversationSessionSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source="device.device_id", read_only=True)
    agent_id = serializers.CharField(source="agent.agent_id", read_only=True)
    spot_id = serializers.CharField(source="spot.spot_id", allow_null=True, read_only=True)
    messages = ConversationMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ConversationSession
        fields = [
            "session_id", "official_session_id", "device_id", "agent_id", "spot_id", "source", "started_at",
            "ended_at", "summary", "knowledge_summary", "status", "messages",
        ]


class ConversationSessionWriteSerializer(serializers.ModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(source="device", queryset=Device.objects.all())
    agent_id = serializers.PrimaryKeyRelatedField(source="agent", queryset=Agent.objects.all())
    spot_id = serializers.PrimaryKeyRelatedField(
        source="spot", queryset=ScenicSpot.objects.all(),
        allow_null=True, required=False,
    )
    messages = ConversationMessageSerializer(many=True, required=False)

    class Meta:
        model = ConversationSession
        fields = [
            "session_id", "official_session_id", "device_id", "agent_id", "spot_id", "source", "started_at",
            "ended_at", "summary", "knowledge_summary", "status", "messages",
        ]
        read_only_fields = ["session_id"]

    def create(self, validated_data):
        messages = validated_data.pop("messages", [])
        session = ConversationSession.objects.create(**validated_data)
        for message in messages:
            message.pop("session", None)
            ConversationMessage.objects.create(session=session, **message)
        return session


class DeviceConversationEventSerializer(serializers.Serializer):
    official_session_id = serializers.CharField(max_length=128)
    role = serializers.ChoiceField(choices=[
        ConversationMessage.Role.USER,
        ConversationMessage.Role.ASSISTANT,
    ])
    content = serializers.CharField(max_length=20000, trim_whitespace=False)
    content_source = serializers.CharField(max_length=80, required=False, default="xiaozhi_official_device_log")
    session_source = serializers.CharField(max_length=80, required=False, default="xiaozhi_official")
    agent_id = serializers.CharField(max_length=64, required=False, allow_blank=True)
    spot_id = serializers.PrimaryKeyRelatedField(
        source="spot", queryset=ScenicSpot.objects.all(), required=False, allow_null=True
    )
    created_at = serializers.DateTimeField(required=False, default=timezone.now)
    metadata = serializers.JSONField(required=False, default=dict)

    def validate_official_session_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("This field may not be blank.")
        return value.strip()

    def validate_metadata(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Expected an object.")
        return sanitize_snapshot(value)


class OfficialSyncLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialSyncLog
        fields = [
            "sync_id", "target_type", "target_id", "payload_snapshot", "sync_mode",
            "status", "operator", "created_at", "synced_at", "note", "failure_reason",
        ]
        read_only_fields = ["sync_id", "created_at"]

    def validate_payload_snapshot(self, value):
        return sanitize_snapshot(value)

    def validate(self, attrs):
        target_type = attrs.get("target_type", getattr(self.instance, "target_type", None))
        target_id = attrs.get("target_id", getattr(self.instance, "target_id", None))
        if target_type == OfficialSyncLog.TargetType.AGENT and target_id:
            agent = Agent.objects.filter(pk=target_id).first()
            if agent is None:
                raise serializers.ValidationError({"target_id": "Agent does not exist."})
            if not attrs.get("payload_snapshot") and self.instance is None:
                attrs["payload_snapshot"] = sanitize_snapshot(agent.official_sync_snapshot())
        status = attrs.get("status")
        if status == OfficialSyncLog.Status.SYNCED and not attrs.get("synced_at"):
            attrs["synced_at"] = timezone.now()
        elif status:
            attrs["synced_at"] = None
        return attrs

    def create(self, validated_data):
        row = super().create(validated_data)
        self._update_agent(row)
        return row

    def update(self, instance, validated_data):
        row = super().update(instance, validated_data)
        self._update_agent(row)
        return row

    @staticmethod
    def _update_agent(row):
        if row.target_type != OfficialSyncLog.TargetType.AGENT:
            return
        agent = Agent.objects.filter(pk=row.target_id).first()
        if agent is None:
            return
        status_map = {
            OfficialSyncLog.Status.PENDING: Agent.OfficialSyncStatus.NOT_SYNCED,
            OfficialSyncLog.Status.SYNCED: Agent.OfficialSyncStatus.SYNCED,
            OfficialSyncLog.Status.FAILED: Agent.OfficialSyncStatus.FAILED,
            OfficialSyncLog.Status.MANUAL_REQUIRED: Agent.OfficialSyncStatus.MANUAL_REQUIRED,
        }
        agent.official_sync_status = status_map[row.status]
        agent.official_synced_at = row.synced_at if row.status == OfficialSyncLog.Status.SYNCED else None
        agent.official_sync_operator = row.operator
        agent.official_sync_note = row.note
        agent.official_sync_failure_reason = row.failure_reason
        agent.save(update_fields=[
            "official_sync_status", "official_synced_at", "official_sync_operator",
            "official_sync_note", "official_sync_failure_reason",
        ])
