from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils import timezone

from apps.agents.models import Agent
from apps.checkins.models import Checkin
from apps.datasets.models import Dataset
from apps.devices.models import Device, DeviceBinding
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


class HardwareBaselineCommandTests(TestCase):
    def setUp(self):
        dataset = Dataset.objects.create(dataset_id="dataset_spot_demo_001", name="D", status=Dataset.Status.CHUNKED)
        agent = Agent.objects.create(agent_id="agent_alo", name="A", personality_prompt="P", dataset=dataset, status=Agent.Status.ACTIVE)
        self.spot = ScenicSpot.objects.create(spot_id="spot_gate_001", name="S", latitude=1, longitude=1, dataset=dataset)
        self.placeholder = NfcTag.objects.create(tag_id="04AABBCCDD", spot=self.spot, label="景区入口占位标签")
        self.device = Device.objects.create(
            device_id="device_001",
            sn="SN-HW",
            online_status=Device.Status.ONLINE,
            last_seen_at=timezone.now(),
            firmware_version="manual-smoke",
            battery_percent=99,
            last_gps_status="fixed",
            last_latitude=1,
            last_longitude=1,
            last_location_quality={"fix": True},
            last_location_at=timezone.now(),
        )
        self.device.set_token("demo-device-token")
        self.device.save()
        DeviceBinding.objects.create(device=self.device, agent=agent)
        Checkin.objects.create(
            device=self.device,
            agent=agent,
            spot=self.spot,
            tag=self.placeholder,
            result=Checkin.Result.SIMULATED,
            source=Checkin.Source.SIMULATION,
            checked_in_at=timezone.now(),
        )

    def test_reset_is_repeatable_and_preserves_configuration(self):
        token_hash = self.device.device_token_hash
        other = Device.objects.create(device_id="simulator_001", sn="SN-SIM", online_status=Device.Status.ONLINE, last_seen_at=timezone.now())
        other.set_token("simulator-token")
        other.save()
        for _ in range(2):
            call_command("reset_hw_test_data", stdout=StringIO())
        self.device.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(Checkin.objects.count(), 0)
        self.assertEqual(self.device.online_status, Device.Status.UNKNOWN)
        self.assertIsNone(self.device.last_seen_at)
        self.assertIsNone(self.device.last_latitude)
        self.assertEqual(self.device.last_location_quality, {})
        self.assertEqual(self.device.device_token_hash, token_hash)
        self.assertEqual(other.online_status, Device.Status.UNKNOWN)
        self.assertIsNone(other.last_seen_at)
        self.assertEqual(self.device.binding.agent_id, "agent_alo")
        self.assertTrue(ScenicSpot.objects.filter(pk="spot_gate_001").exists())
        self.assertTrue(NfcTag.objects.filter(pk="04AABBCCDD", status=NfcTag.Status.ACTIVE).exists())

    def test_real_uid_replaces_placeholder_and_is_idempotent(self):
        call_command("set_hw_nfc_tag", "04:11:22:33", stdout=StringIO())
        call_command("set_hw_nfc_tag", "04-11-22-33", stdout=StringIO())
        self.assertTrue(NfcTag.objects.filter(pk="04112233", status=NfcTag.Status.ACTIVE).exists())
        self.assertFalse(NfcTag.objects.filter(pk="04AABBCCDD", status=NfcTag.Status.ACTIVE).exists())

    def test_referenced_placeholder_is_disabled(self):
        call_command("set_hw_nfc_tag", "04:11:22:33", stdout=StringIO())
        self.placeholder.refresh_from_db()
        self.assertEqual(self.placeholder.status, NfcTag.Status.DISABLED)

    def test_invalid_or_placeholder_uid_is_rejected(self):
        with self.assertRaises(CommandError):
            call_command("set_hw_nfc_tag", "not-a-uid", stdout=StringIO())
        with self.assertRaises(CommandError):
            call_command("set_hw_nfc_tag", "04AABBCCDD", stdout=StringIO())
