import hashlib
import secrets

from django.db import models


class Device(models.Model):
    class Status(models.TextChoices):
        ONLINE = "online"
        OFFLINE = "offline"
        UNKNOWN = "unknown"
        CONFIG_ERROR = "config_error"

    device_id = models.CharField(max_length=64, primary_key=True)
    sn = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=200, blank=True)
    device_token_hash = models.CharField(max_length=64, editable=False)
    device_token_ref = models.CharField(max_length=32, blank=True, editable=False)
    online_status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNKNOWN)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    firmware_version = models.CharField(max_length=80, blank=True)
    battery_percent = models.PositiveSmallIntegerField(null=True, blank=True)
    last_gps_status = models.CharField(max_length=40, blank=True)
    last_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    last_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    last_location_quality = models.JSONField(default=dict, blank=True)
    last_location_at = models.DateTimeField(null=True, blank=True)

    def set_token(self, token):
        self.device_token_hash = hashlib.sha256(token.encode()).hexdigest()
        self.device_token_ref = f"{token[:3]}***{token[-3:]}" if len(token) >= 8 else "***"

    def check_token(self, token):
        digest = hashlib.sha256(token.encode()).hexdigest()
        return secrets.compare_digest(self.device_token_hash, digest)

    def __str__(self):
        return self.name or self.device_id


class DeviceBinding(models.Model):
    class Type(models.TextChoices):
        FACTORY = "factory"
        ADMIN_OVERRIDE = "admin_override"
        DEMO = "demo"

    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name="binding")
    agent = models.ForeignKey("agents.Agent", on_delete=models.PROTECT, related_name="bindings")
    bound_by = models.CharField(max_length=150, blank=True)
    bound_at = models.DateTimeField(auto_now=True)
    binding_type = models.CharField(max_length=24, choices=Type.choices, default=Type.DEMO)
    reason = models.TextField(blank=True)


class BindingEvent(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    agent = models.ForeignKey("agents.Agent", on_delete=models.PROTECT)
    bound_by = models.CharField(max_length=150, blank=True)
    bound_at = models.DateTimeField(auto_now_add=True)
    binding_type = models.CharField(max_length=24, choices=DeviceBinding.Type.choices)
    reason = models.TextField(blank=True)

    class Meta:
        ordering = ["-bound_at"]
