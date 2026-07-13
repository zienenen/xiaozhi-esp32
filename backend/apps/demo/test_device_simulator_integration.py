import sys
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase

from apps.agents.models import Agent
from apps.checkins.models import Checkin
from apps.datasets.models import Dataset
from apps.devices.models import Device, DeviceBinding
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


SIMULATOR_DIR = Path(__file__).resolve().parents[3] / "tools" / "device_simulator"
sys.path.insert(0, str(SIMULATOR_DIR))
import simulate_device as simulator  # noqa: E402


class DeviceSimulatorHttpIntegrationTests(LiveServerTestCase):
    def setUp(self):
        get_user_model().objects.create_user("sim_tester", password="sim-password", is_staff=True)
        dataset = Dataset.objects.create(dataset_id="dataset_sim", name="Simulator", status=Dataset.Status.CHUNKED)
        agent = Agent.objects.create(agent_id="agent_sim", name="Alo", personality_prompt="Guide", dataset=dataset, status=Agent.Status.ACTIVE)
        spot = ScenicSpot.objects.create(spot_id="spot_sim", name="Gate", latitude=31.2, longitude=121.4, dataset=dataset)
        NfcTag.objects.create(tag_id="TAG-SIM", spot=spot)
        device = Device.objects.create(device_id="device_sim", sn="SIM-SN")
        device.set_token("device-secret")
        device.save()
        DeviceBinding.objects.create(device=device, agent=agent)
        self.settings = simulator.Settings(
            f"{self.live_server_url}/api/v1", "device_sim", "device-secret",
            "sim_tester", "sim-password", "spot_sim", "TAG-SIM", 31.2, 121.4, 5,
        )

    def test_real_http_flow_updates_backend_and_marks_simulation(self):
        config = simulator.pull_config(self.settings)
        simulator.heartbeat(self.settings)
        simulator.location(self.settings, event_type="location_update")
        nearby = simulator.location(self.settings, event_type="near_spot")
        first = simulator.checkin(self.settings)
        second = simulator.checkin(self.settings)
        overview = simulator.request_json(self.settings, "GET", "demo/overview", headers=self.settings.admin_headers)["data"]

        device = Device.objects.get(pk="device_sim")
        checkin = Checkin.objects.get()
        self.assertEqual(config["data"]["agent"]["agent_id"], "agent_sim")
        self.assertEqual(device.online_status, Device.Status.ONLINE)
        self.assertEqual(float(device.last_latitude), 31.2)
        self.assertEqual(nearby["data"]["event_type"], "near_spot")
        self.assertEqual(first["data"]["result"], "simulated")
        self.assertEqual(second["data"]["result"], "duplicate")
        self.assertEqual(checkin.source, Checkin.Source.SIMULATION)
        self.assertEqual(overview["device"]["device_id"], "device_sim")
        self.assertTrue(overview["gps"]["near_spot"])
        self.assertEqual(overview["latest_checkin"]["source"], "simulation")
        self.assertEqual(overview["dataset"]["dataset_id"], "dataset_sim")

    def test_unknown_tag_and_invalid_device_credentials_fail(self):
        with self.assertRaisesRegex(simulator.SimulatorError, "tag_unknown"):
            simulator.checkin(self.settings, "UNKNOWN_TAG")
        invalid = simulator.Settings(
            self.settings.base_url, self.settings.device_id, "wrong-token",
            self.settings.admin_username, self.settings.admin_password, self.settings.spot_id,
            self.settings.tag_id, self.settings.latitude, self.settings.longitude, self.settings.timeout,
        )
        with self.assertRaisesRegex(simulator.SimulatorError, "invalid_device_token"):
            simulator.pull_config(invalid)
