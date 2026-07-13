import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from apps.agents.models import Agent
from apps.datasets.models import Dataset
from apps.devices.models import Device
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


class DemoSeedTests(TestCase):
    def test_seed_is_idempotent_and_hashes_device_token(self):
        env = {"DEMO_DEVICE_TOKEN": "seed-device-secret", "DEMO_ADMIN_USERNAME": "demo_admin", "DEMO_ADMIN_PASSWORD": "seed-password"}
        with patch.dict(os.environ, env):
            call_command("seed_demo", verbosity=0)
            call_command("seed_demo", verbosity=0)
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(Agent.objects.count(), 2)
        self.assertEqual(ScenicSpot.objects.count(), 1)
        self.assertEqual(NfcTag.objects.count(), 1)
        self.assertEqual(Dataset.objects.count(), 1)
        device = Device.objects.get()
        self.assertTrue(device.check_token("seed-device-secret"))
        self.assertNotIn("seed-device-secret", device.device_token_hash)
        self.assertTrue(get_user_model().objects.get(username="demo_admin").check_password("seed-password"))
