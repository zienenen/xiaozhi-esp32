from rest_framework import serializers

from apps.datasets.models import Dataset
from .models import Agent


class AgentSerializer(serializers.ModelSerializer):
    dataset_id = serializers.PrimaryKeyRelatedField(source="dataset", queryset=Dataset.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Agent
        fields = ["agent_id", "name", "personality_prompt", "voice_id", "dataset_id", "status", "series", "rarity"]
