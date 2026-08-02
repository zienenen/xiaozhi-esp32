from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.agents.models import Agent
from apps.datasets.models import Dataset
from apps.devices.models import Device, DeviceBinding
from apps.spots.models import ScenicSpot
from .models import ConversationMessage, ConversationSession, OfficialSyncLog


class ConversationAndSyncApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="admin", password="test")
        self.client.force_authenticate(self.user)
        self.dataset = Dataset.objects.create(
            dataset_id="dataset_1", name="Dataset", source_type="manual", status=Dataset.Status.CHUNKED
        )
        self.agent = Agent.objects.create(
            agent_id="agent_1", name="Guide", personality_prompt="Be helpful",
            voice_id="voice_1", dataset=self.dataset, status=Agent.Status.ACTIVE,
        )
        self.device = Device.objects.create(device_id="device_1", sn="SN-1")
        self.device.set_token("device-secret")
        self.device.save()
        DeviceBinding.objects.create(device=self.device, agent=self.agent)
        self.device_headers = {
            "HTTP_X_DEVICE_ID": self.device.pk,
            "HTTP_X_DEVICE_TOKEN": "device-secret",
        }
        self.spot = ScenicSpot.objects.create(
            spot_id="spot_1", name="Entrance", latitude=26.1, longitude=119.3,
            gps_radius_meters=50, dataset=self.dataset,
        )

    def test_conversation_session_list_detail_and_create(self):
        response = self.client.post("/api/v1/conversation-sessions", {
            "device_id": self.device.pk,
            "agent_id": self.agent.pk,
            "spot_id": self.spot.pk,
            "source": "device_log",
            "started_at": timezone.now().isoformat(),
            "summary": "A real-device import-shaped conversation.",
            "knowledge_summary": [{"source_ref": "dataset_1#chunk_1", "summary": "Entrance history"}],
            "status": "closed",
            "messages": [
                {
                    "role": "user", "content": "Tell me about this place.",
                    "content_source": "device_log", "created_at": timezone.now().isoformat(),
                    "metadata": {"official_session_id": "official-1"},
                },
                {
                    "role": "assistant", "content": "Here is its history.",
                    "content_source": "device_log", "created_at": timezone.now().isoformat(),
                },
            ],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        session_id = response.data["data"]["session_id"]
        self.assertEqual(len(response.data["data"]["messages"]), 2)

        response = self.client.get("/api/v1/conversation-sessions", {"device_id": self.device.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        response = self.client.get(f"/api/v1/conversation-sessions/{session_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["agent_id"], self.agent.pk)

    def test_official_sync_log_snapshot_is_generated_sanitized_and_updates_agent(self):
        response = self.client.post("/api/v1/official-sync-logs", {
            "target_type": "agent",
            "target_id": self.agent.pk,
            "payload_snapshot": {
                "personality_prompt": "Be helpful",
                "device_token": "must-not-leak",
                "nested": {"authorization": "Bearer secret"},
            },
            "sync_mode": "manual_copy",
            "status": "pending",
            "note": "Ready for copy",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        sync_id = response.data["data"]["sync_id"]
        snapshot = response.data["data"]["payload_snapshot"]
        self.assertEqual(snapshot["device_token"], "***")
        self.assertEqual(snapshot["nested"]["authorization"], "***")

        response = self.client.patch(f"/api/v1/official-sync-logs/{sync_id}", {
            "status": "synced", "operator": "operator_a"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.agent.refresh_from_db()
        self.assertEqual(self.agent.official_sync_status, Agent.OfficialSyncStatus.SYNCED)
        self.assertIsNotNone(self.agent.official_synced_at)

        response = self.client.get("/api/v1/official-sync-logs", {"target_id": self.agent.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)

    def test_agent_configuration_change_increments_version_and_marks_not_synced(self):
        self.agent.official_sync_status = Agent.OfficialSyncStatus.SYNCED
        self.agent.official_synced_at = timezone.now()
        self.agent.save(update_fields=["official_sync_status", "official_synced_at"])
        response = self.client.patch(f"/api/v1/agents/{self.agent.pk}", {
            "personality_prompt": "A changed prompt",
            "knowledge_references": ["dataset_1#chunk_1"],
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["config_version"], 2)
        self.assertEqual(response.data["data"]["prompt_version"], "v2")
        self.assertEqual(response.data["data"]["official_sync_status"], "not_synced")
        self.assertIsNone(response.data["data"]["official_synced_at"])

    def test_device_events_create_and_reuse_official_session(self):
        created_at = timezone.now().isoformat()
        first = self.client.post("/api/v1/device-conversation-events", {
            "official_session_id": "official-live-1",
            "role": "user",
            "content": "Tell me about this place.",
            "content_source": "xiaozhi_official_device_log",
            "session_source": "xiaozhi_official",
            "spot_id": self.spot.pk,
            "created_at": created_at,
        }, format="json", **self.device_headers)
        second = self.client.post("/api/v1/device-conversation-events", {
            "official_session_id": "official-live-1",
            "role": "assistant",
            "content": "This is the old entrance.",
            "created_at": timezone.now().isoformat(),
        }, format="json", **self.device_headers)

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertTrue(first.data["data"]["session_created"])
        self.assertFalse(second.data["data"]["session_created"])
        self.assertEqual(first.data["data"]["session_id"], second.data["data"]["session_id"])
        session = ConversationSession.objects.get(official_session_id="official-live-1")
        self.assertEqual(session.messages.count(), 2)
        self.assertEqual(
            list(session.messages.values_list("role", flat=True)),
            [ConversationMessage.Role.USER, ConversationMessage.Role.ASSISTANT],
        )

    def test_device_event_uses_backend_binding_instead_of_reported_agent(self):
        other_agent = Agent.objects.create(
            agent_id="agent_wrong", name="Wrong", personality_prompt="Wrong agent"
        )
        response = self.client.post("/api/v1/device-conversation-events", {
            "official_session_id": "official-binding",
            "role": "user",
            "content": "Hello",
            "agent_id": other_agent.pk,
        }, format="json", **self.device_headers)

        self.assertEqual(response.status_code, 201)
        session = ConversationSession.objects.get(official_session_id="official-binding")
        message = session.messages.get()
        self.assertEqual(session.agent_id, self.agent.pk)
        self.assertTrue(message.metadata["agent_binding_overridden"])

    def test_device_event_requires_device_credentials_and_sanitizes_metadata(self):
        payload = {
            "official_session_id": "official-sensitive",
            "role": "assistant",
            "content": "Safe reply",
            "metadata": {
                "device_token": "must-not-leak",
                "nested": {"authorization": "Bearer secret", "confidence": 0.98},
            },
        }
        denied = self.client.post(
            "/api/v1/device-conversation-events",
            payload,
            format="json",
            HTTP_X_DEVICE_ID=self.device.pk,
            HTTP_X_DEVICE_TOKEN="wrong",
        )
        accepted = self.client.post(
            "/api/v1/device-conversation-events", payload, format="json", **self.device_headers
        )

        self.assertEqual(denied.status_code, 401)
        self.assertEqual(denied.data["error"]["code"], "invalid_device_token")
        self.assertEqual(accepted.status_code, 201)
        metadata = ConversationMessage.objects.get().metadata
        self.assertEqual(metadata["device_token"], "***")
        self.assertEqual(metadata["nested"]["authorization"], "***")
        self.assertEqual(metadata["nested"]["confidence"], 0.98)
        self.assertNotIn("device-secret", str(accepted.data))
        self.assertNotIn("must-not-leak", str(accepted.data))

    def test_device_event_rejects_non_conversation_roles(self):
        response = self.client.post("/api/v1/device-conversation-events", {
            "official_session_id": "official-tool",
            "role": "tool",
            "content": "tool output",
        }, format="json", **self.device_headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ConversationSession.objects.count(), 0)
