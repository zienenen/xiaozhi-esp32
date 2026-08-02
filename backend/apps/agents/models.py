from django.db import models


class Agent(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        DISABLED = "disabled"
        DRAFT = "draft"

    class OfficialSyncStatus(models.TextChoices):
        NOT_SYNCED = "not_synced"
        SYNCED = "synced"
        FAILED = "failed"
        MANUAL_REQUIRED = "manual_required"

    agent_id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=120)
    personality_prompt = models.TextField()
    voice_id = models.CharField(max_length=120, blank=True)
    knowledge_references = models.JSONField(default=list, blank=True)
    tool_endpoint_url = models.URLField(blank=True)
    config_version = models.PositiveIntegerField(default=1)
    prompt_version = models.CharField(max_length=64, default="v1")
    official_sync_status = models.CharField(
        max_length=30, choices=OfficialSyncStatus.choices, default=OfficialSyncStatus.NOT_SYNCED
    )
    official_synced_at = models.DateTimeField(null=True, blank=True)
    official_sync_operator = models.CharField(max_length=150, blank=True)
    official_sync_note = models.TextField(blank=True)
    official_sync_failure_reason = models.TextField(blank=True)
    dataset = models.ForeignKey("datasets.Dataset", null=True, blank=True, on_delete=models.SET_NULL, related_name="agents")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    series = models.CharField(max_length=120, blank=True)
    rarity = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.name

    def official_sync_snapshot(self):
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "personality_prompt": self.personality_prompt,
            "voice_id": self.voice_id,
            "knowledge_references": self.knowledge_references,
            "dataset_id": self.dataset_id,
            "tool_endpoint_url": self.tool_endpoint_url,
            "config_version": self.config_version,
            "prompt_version": self.prompt_version,
        }
