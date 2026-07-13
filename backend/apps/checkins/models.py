import uuid

from django.db import models


def checkin_id():
    return f"checkin_{uuid.uuid4().hex}"


class Checkin(models.Model):
    class Result(models.TextChoices):
        SUCCESS = "success"
        DUPLICATE = "duplicate"
        FAILED = "failed"
        SIMULATED = "simulated"

    class Source(models.TextChoices):
        DEVICE = "device"
        SIMULATION = "simulation"

    checkin_id = models.CharField(max_length=64, primary_key=True, default=checkin_id, editable=False)
    device = models.ForeignKey("devices.Device", on_delete=models.PROTECT, related_name="checkins")
    agent = models.ForeignKey("agents.Agent", on_delete=models.PROTECT, related_name="checkins")
    spot = models.ForeignKey("spots.ScenicSpot", on_delete=models.PROTECT, related_name="checkins")
    tag = models.ForeignKey("nfc_tags.NfcTag", null=True, blank=True, on_delete=models.PROTECT, related_name="checkins")
    result = models.CharField(max_length=20, choices=Result.choices)
    failure_code = models.CharField(max_length=64, blank=True)
    source = models.CharField(max_length=20, choices=Source.choices)
    checked_in_at = models.DateTimeField()
    location_quality = models.JSONField(default=dict, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    class Meta:
        ordering = ["-checked_in_at"]
        indexes = [models.Index(fields=["device", "spot", "checked_in_at"])]
