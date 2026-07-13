import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.agents.models import Agent
from apps.datasets.models import Dataset, DatasetChunk
from apps.devices.models import BindingEvent, Device, DeviceBinding
from apps.nfc_tags.models import NfcTag
from apps.spots.models import ScenicSpot


class Command(BaseCommand):
    help = "Create or update the phase-one demo account and business data."

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
            agent, _ = Agent.objects.update_or_create(agent_id=agent_id, defaults={"name": name, "personality_prompt": prompt, "voice_id": voice, "dataset": dataset, "status": Agent.Status.ACTIVE})
            agents.append(agent)
        spot, _ = ScenicSpot.objects.update_or_create(spot_id="spot_gate_001", defaults={"name": "景区入口", "scenic_area_name": "一期演示景区", "latitude": 31.2304, "longitude": 121.4737, "gps_radius_meters": 50, "dataset": dataset, "checkin_message": "你到啦！这里就是我们今天旅程的第一站。", "status": ScenicSpot.Status.ACTIVE})
        NfcTag.objects.update_or_create(tag_id="04AABBCCDD", defaults={"spot": spot, "label": "景区入口标签", "status": NfcTag.Status.ACTIVE})
        device, created = Device.objects.get_or_create(device_id="device_001", defaults={"sn": "DEMO-SN-001", "name": "一期演示机器人"})
        if created or not device.device_token_hash:
            device.set_token(device_token)
            device.save()
        binding, _ = DeviceBinding.objects.update_or_create(device=device, defaults={"agent": agents[0], "binding_type": DeviceBinding.Type.DEMO, "bound_by": "seed_demo"})
        BindingEvent.objects.get_or_create(device=device, agent=binding.agent, binding_type=binding.binding_type, bound_by="seed_demo")

        user, _ = get_user_model().objects.get_or_create(username=username, defaults={"is_staff": True, "is_superuser": True})
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS("Demo data is ready: 1 device, 2 agents, 1 spot, 1 NFC tag and 1 dataset."))
