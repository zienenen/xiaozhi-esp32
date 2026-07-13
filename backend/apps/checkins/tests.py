from django.test import TestCase

from apps.agents.models import Agent
from apps.datasets.models import Dataset
from apps.devices.models import Device, DeviceBinding
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot
from .models import Checkin
from .services import create_checkin


class CheckinServiceEdgeTests(TestCase):
    def setUp(self):
        dataset = Dataset.objects.create(dataset_id="d", name="D")
        agent = Agent.objects.create(agent_id="a", name="A", personality_prompt="P", dataset=dataset)
        self.device = Device.objects.create(device_id="dev", sn="sn")
        DeviceBinding.objects.create(device=self.device, agent=agent)
        self.spot = ScenicSpot.objects.create(spot_id="s1", name="S1", latitude=1, longitude=1)
        self.other_spot = ScenicSpot.objects.create(spot_id="s2", name="S2", latitude=2, longitude=2)
        self.tag = NfcTag.objects.create(tag_id="tag", spot=self.spot)

    def test_spot_mismatch(self):
        checkin, code = create_checkin(device=self.device, spot_id=self.other_spot.pk, tag_id=self.tag.pk, source=Checkin.Source.DEVICE)
        self.assertIsNone(checkin)
        self.assertEqual(code, "spot_mismatch")

    def test_disabled_spot(self):
        self.spot.status = ScenicSpot.Status.DISABLED
        self.spot.save()
        checkin, code = create_checkin(device=self.device, spot_id=self.spot.pk, tag_id=self.tag.pk, source=Checkin.Source.DEVICE)
        self.assertIsNone(checkin)
        self.assertEqual(code, "spot_disabled")
