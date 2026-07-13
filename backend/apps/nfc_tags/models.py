from django.db import models


class NfcTag(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        DISABLED = "disabled"
        UNKNOWN = "unknown"

    tag_id = models.CharField(max_length=128, primary_key=True)
    spot = models.ForeignKey("spots.ScenicSpot", on_delete=models.PROTECT, related_name="nfc_tags")
    label = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.label or self.tag_id
