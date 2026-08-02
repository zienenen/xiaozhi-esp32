import re

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models.deletion import ProtectedError

from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


PLACEHOLDER_TAG_ID = "04AABBCCDD"
PN532_UID_LENGTHS = {8, 14, 20}


def normalize_uid(value):
    uid = re.sub(r"[\s:\-]", "", value).upper()
    if not re.fullmatch(r"[0-9A-F]+", uid or "") or len(uid) not in PN532_UID_LENGTHS:
        raise CommandError("PN532 UID must contain 4, 7, or 10 bytes of hexadecimal data")
    return uid


def normalize_tag_id(value):
    tag_id = re.sub(r"[\s:\-]", "", value).upper()
    if not re.fullmatch(r"[0-9A-F]+", tag_id or ""):
        raise CommandError("NFC tag ID must contain hexadecimal data")
    return tag_id


class Command(BaseCommand):
    help = "Replace the demo placeholder NFC tag with a UID read from a real PN532."

    def add_arguments(self, parser):
        parser.add_argument("tag_id", help="Real PN532 UID, with or without ':'/'-' separators")
        parser.add_argument("--placeholder-id", default=PLACEHOLDER_TAG_ID)
        parser.add_argument("--spot-id", default="spot_gate_001")

    @transaction.atomic
    def handle(self, *args, **options):
        tag_id = normalize_uid(options["tag_id"])
        placeholder_id = normalize_tag_id(options["placeholder_id"])
        if tag_id == placeholder_id:
            raise CommandError("The real PN532 UID must not equal the demo placeholder UID")
        try:
            spot = ScenicSpot.objects.get(pk=options["spot_id"])
        except ScenicSpot.DoesNotExist as exc:
            raise CommandError(f"Spot does not exist: {options['spot_id']}") from exc

        placeholder = NfcTag.objects.filter(pk=placeholder_id).first()
        label = placeholder.label if placeholder else f"PN532 {tag_id}"
        real_tag, created = NfcTag.objects.update_or_create(
            tag_id=tag_id,
            defaults={"spot": spot, "label": label.replace("占位", "真实") if label else f"PN532 {tag_id}", "status": NfcTag.Status.ACTIVE},
        )

        placeholder_action = "not_found"
        if placeholder:
            try:
                placeholder.delete()
                placeholder_action = "deleted"
            except ProtectedError:
                placeholder.status = NfcTag.Status.DISABLED
                placeholder.save(update_fields=["status"])
                placeholder_action = "disabled_referenced"

        self.stdout.write(
            self.style.SUCCESS(
                f"Real NFC tag ready: tag_id={real_tag.tag_id}, spot={real_tag.spot_id}, "
                f"created={created}, placeholder={placeholder_action}"
            )
        )
        self.stdout.write("Verify this tag_id on the NFC management page before hardware acceptance.")
