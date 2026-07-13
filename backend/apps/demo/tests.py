from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.agents.models import Agent
from apps.checkins.models import Checkin
from apps.datasets.models import Dataset, DatasetChunk
from apps.devices.models import Device, DeviceBinding
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


class BackendContractTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("tester", password="test", is_staff=True)
        self.dataset = Dataset.objects.create(dataset_id="dataset_1", name="Demo", status=Dataset.Status.CHUNKED)
        DatasetChunk.objects.create(dataset=self.dataset, title="入口历史", summary="入口建于测试年代", source_ref="demo#1")
        self.agent = Agent.objects.create(agent_id="agent_1", name="Alo", personality_prompt="Helpful guide", dataset=self.dataset, status=Agent.Status.ACTIVE)
        self.spot = ScenicSpot.objects.create(spot_id="spot_1", name="Gate", latitude=31.2, longitude=121.4, dataset=self.dataset, checkin_message="Welcome")
        self.tag = NfcTag.objects.create(tag_id="TAG-1", spot=self.spot)
        self.device = Device.objects.create(device_id="device_1", sn="SN-1", name="Robot")
        self.device.set_token("device-secret")
        self.device.save()
        DeviceBinding.objects.create(device=self.device, agent=self.agent)
        self.device_headers = {"HTTP_X_DEVICE_ID": "device_1", "HTTP_X_DEVICE_TOKEN": "device-secret"}

    def test_device_config_and_token_is_not_exposed(self):
        response = self.client.get("/api/v1/device-config?device_id=device_1", **self.device_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["agent"]["agent_id"], "agent_1")
        self.assertNotIn("device-secret", str(response.data))

    def test_invalid_device_token_is_generic(self):
        response = self.client.get("/api/v1/device-config?device_id=device_1", HTTP_X_DEVICE_ID="device_1", HTTP_X_DEVICE_TOKEN="wrong")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["error"]["code"], "invalid_device_token")
        self.assertNotIn("wrong", str(response.data))

    def test_heartbeat_updates_last_seen(self):
        response = self.client.post("/api/v1/device-heartbeats", {"device_id": "device_1", "firmware_version": "1.0", "battery_percent": 82, "gps_status": "fixed"}, format="json", **self.device_headers)
        self.assertEqual(response.status_code, 200)
        self.device.refresh_from_db()
        self.assertEqual(self.device.online_status, "online")
        self.assertEqual(self.device.battery_percent, 82)

    def test_location_only_replaces_latest_summary(self):
        payload = {"device_id": "device_1", "spot_id": "spot_1", "event_type": "near_spot", "latitude": 31.21, "longitude": 121.41, "location_quality": {"fix": True, "satellites": 8, "hdop": 1.2}, "event_time": timezone.now().isoformat()}
        response = self.client.post("/api/v1/location-events", payload, format="json", **self.device_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Checkin.objects.count(), 0)
        self.device.refresh_from_db()
        self.assertEqual(self.device.last_location_quality["satellites"], 8)

    def test_checkin_success_and_duplicate(self):
        payload = {"device_id": "device_1", "spot_id": "spot_1", "tag_id": "TAG-1", "source": "device", "event_time": timezone.now().isoformat()}
        first = self.client.post("/api/v1/checkins", payload, format="json", **self.device_headers)
        second = self.client.post("/api/v1/checkins", payload, format="json", **self.device_headers)
        self.assertEqual(first.data["data"]["result"], "success")
        self.assertEqual(second.data["data"]["result"], "duplicate")
        self.assertEqual(Checkin.objects.count(), 1)

    def test_checkin_business_errors(self):
        base = {"device_id": "device_1", "spot_id": "spot_1", "source": "device"}
        unknown = self.client.post("/api/v1/checkins", {**base, "tag_id": "UNKNOWN"}, format="json", **self.device_headers)
        self.assertEqual(unknown.data["error"]["code"], "tag_unknown")
        self.tag.status = NfcTag.Status.DISABLED
        self.tag.save()
        disabled = self.client.post("/api/v1/checkins", {**base, "tag_id": "TAG-1"}, format="json", **self.device_headers)
        self.assertEqual(disabled.data["error"]["code"], "tag_disabled")

    def test_unbound_device_error(self):
        self.device.binding.delete()
        response = self.client.post("/api/v1/checkins", {"device_id": "device_1", "spot_id": "spot_1", "tag_id": "TAG-1"}, format="json", **self.device_headers)
        self.assertEqual(response.data["error"]["code"], "device_not_bound")

    def test_simulation_requires_staff_and_marks_source(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/v1/demo/simulate-checkin", {"device_id": "device_1", "spot_id": "spot_1", "tag_id": "TAG-1"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["source"], "simulation")
        self.assertEqual(Checkin.objects.get().source, Checkin.Source.SIMULATION)

    def test_tool_endpoints_require_tool_token(self):
        denied = self.client.get("/api/v1/agents/agent_1/context")
        allowed = self.client.get("/api/v1/agents/agent_1/context", HTTP_X_TOOL_TOKEN="test-tool-token")
        search = self.client.post("/api/v1/knowledge/search", {"query": "入口", "dataset_id": "dataset_1"}, format="json", HTTP_X_TOOL_TOKEN="test-tool-token")
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(allowed.status_code, 200)
        self.assertEqual(len(search.data["data"]["results"]), 1)

    def test_authenticated_management_and_overview(self):
        self.client.force_authenticate(self.user)
        devices = self.client.get("/api/v1/devices")
        overview = self.client.get("/api/v1/demo/overview")
        datasets = self.client.get("/api/v1/datasets")
        self.assertEqual(devices.status_code, 200)
        self.assertEqual(overview.data["data"]["summary"]["device_count"], 1)
        self.assertEqual(overview.data["data"]["device"]["device_id"], "device_1")
        self.assertEqual(overview.data["data"]["agent"]["agent_id"], "agent_1")
        self.assertEqual(overview.data["data"]["dataset"]["dataset_id"], "dataset_1")
        self.assertEqual(datasets.data["data"][0]["chunk_count"], 1)
