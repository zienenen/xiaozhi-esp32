from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.agents.models import Agent
from apps.checkins.models import Checkin
from apps.conversations.models import ConversationMessage, ConversationSession
from apps.datasets.models import Dataset, DatasetChunk
from apps.devices.models import Device, DeviceBinding
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


class UserAggregationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(get_user_model().objects.create_user("user"))
        self.dataset = Dataset.objects.create(
            dataset_id="dataset_user", name="User map", status=Dataset.Status.VECTORIZED
        )
        DatasetChunk.objects.create(dataset=self.dataset, title="History", summary="Summary")
        self.agent = Agent.objects.create(
            agent_id="agent_user",
            name="Guide",
            personality_prompt="Guide the visitor",
            dataset=self.dataset,
            status=Agent.Status.ACTIVE,
        )
        self.device = Device.objects.create(
            device_id="device_user",
            sn="SN-USER",
            name="Visitor device",
            online_status=Device.Status.ONLINE,
            last_seen_at=timezone.now(),
            last_gps_status="fixed",
            last_latitude=26.0861000,
            last_longitude=119.2911000,
            last_location_at=timezone.now(),
        )
        self.device.set_token("device-token")
        self.device.save()
        DeviceBinding.objects.create(device=self.device, agent=self.agent, bound_by="factory")
        self.spot = ScenicSpot.objects.create(
            spot_id="spot_user",
            name="Gate",
            latitude=26.0861000,
            longitude=119.2911000,
            gps_radius_meters=50,
            dataset=self.dataset,
        )
        self.other_spot = ScenicSpot.objects.create(
            spot_id="spot_other",
            name="Hall",
            latitude=26.0961000,
            longitude=119.3011000,
            dataset=self.dataset,
        )
        self.tag = NfcTag.objects.create(tag_id="TAG-USER", spot=self.spot)
        self.session = ConversationSession.objects.create(
            device=self.device,
            agent=self.agent,
            spot=self.spot,
            source=ConversationSession.Source.DEVICE_LOG,
            started_at=timezone.now(),
            status=ConversationSession.Status.CLOSED,
        )
        ConversationMessage.objects.create(
            session=self.session,
            role=ConversationMessage.Role.USER,
            content="Tell me the story",
            content_source=ConversationMessage.ContentSource.DEVICE_LOG,
            created_at=timezone.now(),
        )
        self.real_checkin = Checkin.objects.create(
            device=self.device,
            agent=self.agent,
            spot=self.spot,
            tag=self.tag,
            result=Checkin.Result.SUCCESS,
            source=Checkin.Source.DEVICE,
            checked_in_at=timezone.now(),
        )
        Checkin.objects.create(
            device=self.device,
            agent=self.agent,
            spot=self.other_spot,
            result=Checkin.Result.SIMULATED,
            source=Checkin.Source.SIMULATION,
            checked_in_at=timezone.now(),
        )

    def test_companion_returns_binding_and_existing_recent_conversations(self):
        response = self.client.get("/api/v1/user/companion")

        self.assertEqual(response.status_code, 200)
        data = response.data["data"]
        self.assertEqual(data["device"]["device_id"], self.device.pk)
        self.assertEqual(data["agent"]["agent_id"], self.agent.pk)
        self.assertEqual(data["binding"]["bound_by"], "factory")
        self.assertEqual(data["recent_conversations"][0]["session_id"], self.session.pk)
        self.assertEqual(data["recent_conversations"][0]["messages"][0]["content"], "Tell me the story")

    def test_map_returns_location_nfc_points_and_only_real_stamps(self):
        response = self.client.get("/api/v1/user/map", {"device_id": self.device.pk})

        self.assertEqual(response.status_code, 200)
        data = response.data["data"]
        points = {point["spot_id"]: point for point in data["points"]}
        self.assertTrue(data["location"]["is_near_spot"])
        self.assertEqual(data["nfc"]["tag_id"], self.tag.pk)
        self.assertEqual(data["stamp_summary"]["earned"], 1)
        self.assertTrue(data["stamp_summary"]["simulation_excluded"])
        self.assertEqual(points[self.spot.pk]["state"], "stamped")
        self.assertEqual(points[self.other_spot.pk]["state"], "available")

    def test_agent_cards_include_aggregate_fields_without_duplicate_counts(self):
        response = self.client.get("/api/v1/agents")

        self.assertEqual(response.status_code, 200)
        card = response.data["data"][0]
        self.assertEqual(card["bound_device_count"], 1)
        self.assertEqual(card["online_device_count"], 1)
        self.assertEqual(card["conversation_count"], 1)
        self.assertEqual(card["dataset_chunk_count"], 1)
        self.assertEqual(card["dataset_status"], "ready")
        self.assertEqual(card["bound_devices"][0]["device_id"], self.device.pk)
