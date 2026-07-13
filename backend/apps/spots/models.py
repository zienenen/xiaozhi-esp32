from django.db import models


class ScenicSpot(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        DISABLED = "disabled"

    spot_id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=200)
    scenic_area_name = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    gps_radius_meters = models.PositiveIntegerField(default=50)
    dataset = models.ForeignKey("datasets.Dataset", null=True, blank=True, on_delete=models.SET_NULL, related_name="spots")
    checkin_message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return self.name
