from datetime import timedelta

from django.utils import timezone

from apps.nfc_tags.models import NfcTag
from .models import Checkin


COOLDOWN_SECONDS = 300


def create_checkin(*, device, spot_id, tag_id, source, event_time=None, location_quality=None):
    try:
        agent = device.binding.agent
    except Exception as exc:
        if exc.__class__.__name__ == "RelatedObjectDoesNotExist":
            return None, "device_not_bound"
        raise
    try:
        tag = NfcTag.objects.select_related("spot").get(pk=tag_id)
    except NfcTag.DoesNotExist:
        return None, "tag_unknown"
    if tag.status != NfcTag.Status.ACTIVE:
        return None, "tag_disabled"
    if tag.spot_id != spot_id:
        return None, "spot_mismatch"
    if tag.spot.status != "active":
        return None, "spot_disabled"
    now = event_time or timezone.now()
    previous = Checkin.objects.filter(
        device=device,
        spot=tag.spot,
        result__in=[Checkin.Result.SUCCESS, Checkin.Result.SIMULATED],
        checked_in_at__gte=now - timedelta(seconds=COOLDOWN_SECONDS),
    ).first()
    if previous:
        return previous, "duplicate"
    result = Checkin.Result.SIMULATED if source == Checkin.Source.SIMULATION else Checkin.Result.SUCCESS
    checkin = Checkin.objects.create(
        device=device,
        agent=agent,
        spot=tag.spot,
        tag=tag,
        result=result,
        source=source,
        checked_in_at=now,
        location_quality=location_quality or {},
        latitude=device.last_latitude,
        longitude=device.last_longitude,
    )
    tag.last_seen_at = now
    tag.save(update_fields=["last_seen_at"])
    return checkin, None
