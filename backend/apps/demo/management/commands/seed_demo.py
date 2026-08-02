import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.agents.models import Agent
from apps.conversations.models import ConversationMessage, ConversationSession, OfficialSyncLog
from apps.datasets.models import Dataset, DatasetChunk
from apps.devices.models import BindingEvent, Device, DeviceBinding
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


class Command(BaseCommand):
    help = "Create demo/simulator data. Run reset_hw_test_data before real hardware acceptance."

    @transaction.atomic
    def handle(self, *args, **options):
        device_token = os.getenv("DEMO_DEVICE_TOKEN")
        username = os.getenv("DEMO_ADMIN_USERNAME")
        password = os.getenv("DEMO_ADMIN_PASSWORD")
        if not all([device_token, username, password]):
            raise CommandError("DEMO_DEVICE_TOKEN, DEMO_ADMIN_USERNAME and DEMO_ADMIN_PASSWORD are required")

        dataset, _ = Dataset.objects.update_or_create(dataset_id="dataset_spot_demo_001", defaults={"name": "景区一期演示数据集", "source_type": "manual", "status": Dataset.Status.CHUNKED})
        DatasetChunk.objects.update_or_create(dataset=dataset, source_ref="demo#entrance", defaults={"title": "景区入口介绍", "summary": "景区入口的历史、游览路线和注意事项。", "sort_order": 1})
        agents = []
        for agent_id, name, prompt, voice in [
            ("agent_alo", "阿洛", "你是活泼、好奇、喜欢讲故事的旅游伙伴。", "voice_alo_01"),
            ("agent_yoyo", "悠悠", "你是沉稳、温暖、善于讲解文化的旅游伙伴。", "voice_yoyo_01"),
        ]:
            agent, _ = Agent.objects.update_or_create(agent_id=agent_id, defaults={
                "name": name,
                "personality_prompt": prompt,
                "voice_id": voice,
                "knowledge_references": ["dataset_spot_demo_001#entrance"],
                "tool_endpoint_url": "https://example.invalid/api/v1/agents/agent_alo/context",
                "dataset": dataset,
                "status": Agent.Status.ACTIVE,
                "prompt_version": "v1",
                "official_sync_status": Agent.OfficialSyncStatus.NOT_SYNCED,
            })
            agents.append(agent)
        spot, _ = ScenicSpot.objects.update_or_create(spot_id="spot_gate_001", defaults={"name": "景区入口", "scenic_area_name": "一期演示景区", "latitude": 31.2304, "longitude": 121.4737, "gps_radius_meters": 50, "dataset": dataset, "checkin_message": "你到啦！这里就是我们今天旅程的第一站。", "status": ScenicSpot.Status.ACTIVE})
        NfcTag.objects.update_or_create(tag_id="04AABBCCDD", defaults={"spot": spot, "label": "景区入口占位标签", "status": NfcTag.Status.ACTIVE})
        device, created = Device.objects.get_or_create(device_id="device_001", defaults={"sn": "DEMO-SN-001", "name": "一期演示机器人"})
        if created or not device.device_token_hash:
            device.set_token(device_token)
            device.save()
        binding, _ = DeviceBinding.objects.update_or_create(device=device, defaults={"agent": agents[0], "binding_type": DeviceBinding.Type.DEMO, "bound_by": "seed_demo"})
        BindingEvent.objects.get_or_create(device=device, agent=binding.agent, binding_type=binding.binding_type, bound_by="seed_demo")

        now = timezone.now()
        session, _ = ConversationSession.objects.update_or_create(
            session_id="session_demo_device_log_001",
            defaults={
                "device": device,
                "agent": agents[0],
                "spot": spot,
                "source": ConversationSession.Source.DEVICE_LOG,
                "started_at": now,
                "ended_at": now,
                "summary": "Demo robot greeting and scenic spot introduction.",
                "knowledge_summary": [{
                    "title": "Scenic entrance introduction",
                    "summary": "Seed reference for the real device conversation import flow.",
                    "source_ref": "demo#entrance",
                }],
                "status": ConversationSession.Status.CLOSED,
            },
        )
        ConversationMessage.objects.update_or_create(
            message_id="message_demo_user_001",
            defaults={
                "session": session,
                "role": ConversationMessage.Role.USER,
                "content": "Please introduce this scenic spot.",
                "content_source": ConversationMessage.ContentSource.DEVICE_LOG,
                "created_at": now,
                "metadata": {"seed_data": True, "acceptance_state": "reference_not_live_evidence"},
            },
        )
        ConversationMessage.objects.update_or_create(
            message_id="message_demo_assistant_001",
            defaults={
                "session": session,
                "role": ConversationMessage.Role.ASSISTANT,
                "content": "Welcome. Let me tell you the story of this place.",
                "content_source": ConversationMessage.ContentSource.DEVICE_LOG,
                "created_at": now,
                "metadata": {"seed_data": True, "acceptance_state": "reference_not_live_evidence"},
            },
        )
        OfficialSyncLog.objects.update_or_create(
            sync_id="sync_demo_agent_alo_001",
            defaults={
                "target_type": OfficialSyncLog.TargetType.AGENT,
                "target_id": agents[0].agent_id,
                "payload_snapshot": agents[0].official_sync_snapshot(),
                "sync_mode": OfficialSyncLog.SyncMode.MANUAL_COPY,
                "status": OfficialSyncLog.Status.PENDING,
                "operator": "seed_demo",
                "note": "Configuration snapshot prepared for manual copy to the official console.",
            },
        )

        user, _ = get_user_model().objects.get_or_create(username=username, defaults={"is_staff": True, "is_superuser": True})
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(
            "Demo data is ready: 1 device, 2 agents, 1 spot, 1 NFC tag, "
            "1 dataset, 1 conversation session and 1 official sync snapshot."
        ))
        self.stdout.write("This is simulator/demo data, not a real hardware acceptance baseline.")
