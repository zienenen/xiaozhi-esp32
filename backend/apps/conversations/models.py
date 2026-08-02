import uuid

from django.db import models


def session_id():
    return f"session_{uuid.uuid4().hex}"


def message_id():
    return f"message_{uuid.uuid4().hex}"


def sync_id():
    return f"sync_{uuid.uuid4().hex}"


class ConversationSession(models.Model):
    class Source(models.TextChoices):
        OFFICIAL_MANUAL_IMPORT = "official_manual_import"
        TOOL_CALLBACK = "tool_callback"
        DEVICE_LOG = "device_log"
        SELF_HOSTED_VOICE = "self_hosted_voice"

    class Status(models.TextChoices):
        OPEN = "open"
        CLOSED = "closed"
        FAILED = "failed"

    session_id = models.CharField(max_length=72, primary_key=True, default=session_id, editable=False)
    official_session_id = models.CharField(max_length=128, null=True, blank=True)
    device = models.ForeignKey("devices.Device", on_delete=models.PROTECT, related_name="conversation_sessions")
    agent = models.ForeignKey("agents.Agent", on_delete=models.PROTECT, related_name="conversation_sessions")
    spot = models.ForeignKey(
        "spots.ScenicSpot", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="conversation_sessions",
    )
    source = models.CharField(max_length=40, choices=Source.choices)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)
    knowledge_summary = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)

    class Meta:
        ordering = ["-started_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["device", "official_session_id"],
                name="unique_device_official_conversation_session",
            ),
        ]
        indexes = [
            models.Index(fields=["device", "started_at"]),
            models.Index(fields=["agent", "started_at"]),
            models.Index(fields=["source", "started_at"]),
        ]


class ConversationMessage(models.Model):
    class Role(models.TextChoices):
        USER = "user"
        ASSISTANT = "assistant"
        SYSTEM = "system"
        TOOL = "tool"

    class ContentSource(models.TextChoices):
        MANUAL = "manual"
        OFFICIAL_EXPORT = "official_export"
        DEVICE_LOG = "device_log"
        API = "api"

    message_id = models.CharField(max_length=72, primary_key=True, default=message_id, editable=False)
    session = models.ForeignKey(ConversationSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=Role.choices)
    content = models.TextField()
    content_source = models.CharField(max_length=30, choices=ContentSource.choices)
    created_at = models.DateTimeField()
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["created_at", "message_id"]
        indexes = [models.Index(fields=["session", "created_at"])]


class OfficialSyncLog(models.Model):
    class TargetType(models.TextChoices):
        AGENT = "agent"
        DEVICE = "device"
        TOOL = "tool"
        VOICE = "voice"

    class SyncMode(models.TextChoices):
        MANUAL_COPY = "manual_copy"
        SEMI_AUTO = "semi_auto"
        API = "api"

    class Status(models.TextChoices):
        PENDING = "pending"
        SYNCED = "synced"
        FAILED = "failed"
        MANUAL_REQUIRED = "manual_required"

    sync_id = models.CharField(max_length=72, primary_key=True, default=sync_id, editable=False)
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.CharField(max_length=128)
    payload_snapshot = models.JSONField(default=dict)
    sync_mode = models.CharField(max_length=20, choices=SyncMode.choices, default=SyncMode.MANUAL_COPY)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    operator = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    synced_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    failure_reason = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["target_type", "target_id", "created_at"]),
            models.Index(fields=["status", "created_at"]),
        ]
