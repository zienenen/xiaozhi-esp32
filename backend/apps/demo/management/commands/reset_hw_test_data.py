from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.checkins.models import Checkin
from apps.devices.models import Device, DeviceBinding
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


class Command(BaseCommand):
    help = (
        "Reset event and runtime state before real ESP32 acceptance while preserving "
        "the device token, binding, spots, NFC tags, agents, and datasets."
    )

    def add_arguments(self, parser):
        parser.add_argument("--device-id", default="device_001")

    @transaction.atomic
    def handle(self, *args, **options):
        device_id = options["device_id"]
        try:
            device = Device.objects.select_related("binding__agent").get(pk=device_id)
        except Device.DoesNotExist as exc:
            raise CommandError(f"Required hardware device does not exist: {device_id}") from exc
        try:
            binding = device.binding
        except DeviceBinding.DoesNotExist as exc:
            raise CommandError(f"Required hardware device is not bound: {device_id}") from exc

        active_spots = ScenicSpot.objects.filter(status=ScenicSpot.Status.ACTIVE)
        active_tags = NfcTag.objects.filter(status=NfcTag.Status.ACTIVE, spot__in=active_spots)
        if not binding.agent.dataset_id or not active_spots.exists() or not active_tags.exists():
            raise CommandError("Hardware baseline is incomplete: active dataset, spot, and NFC tag are required")

        deleted_checkins, _ = Checkin.objects.all().delete()
        reset_devices = Device.objects.update(
            online_status=Device.Status.UNKNOWN,
            last_seen_at=None,
            firmware_version="",
            battery_percent=None,
            last_gps_status="",
            last_latitude=None,
            last_longitude=None,
            last_location_quality={},
            last_location_at=None,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Hardware baseline reset: device={device_id}, checkins_deleted={deleted_checkins}, "
                f"devices_reset={reset_devices}, "
                f"online_status=unknown, binding={binding.agent_id}, active_tags={active_tags.count()}"
            )
        )
        self.stdout.write("No real ESP32 acceptance result was created by this command.")
