from django.shortcuts import get_object_or_404
from django.db.models import Count, Max, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.checkins.models import Checkin
from config.api import ToolTokenPermission, envelope
from .models import Agent
from .serializers import AgentSerializer


def agent_card_queryset():
    return Agent.objects.select_related("dataset").prefetch_related("bindings__device").annotate(
        dataset_chunk_count=Count("dataset__chunks", distinct=True),
        bound_device_count=Count("bindings", distinct=True),
        online_device_count=Count(
            "bindings", filter=Q(bindings__device__online_status="online"), distinct=True
        ),
        conversation_count=Count("conversation_sessions", distinct=True),
        latest_conversation_at=Max("conversation_sessions__started_at"),
        latest_checkin_at=Max("checkins__checked_in_at"),
    )


class AgentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return envelope(AgentSerializer(agent_card_queryset(), many=True).data)

    def post(self, request):
        serializer = AgentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        agent = serializer.save()
        return envelope(
            AgentSerializer(get_object_or_404(agent_card_queryset(), pk=agent.pk)).data,
            status=201,
        )


class AgentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, agent_id):
        return envelope(AgentSerializer(get_object_or_404(agent_card_queryset(), pk=agent_id)).data)

    def patch(self, request, agent_id):
        serializer = AgentSerializer(get_object_or_404(Agent, pk=agent_id), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return envelope(
            AgentSerializer(get_object_or_404(agent_card_queryset(), pk=agent_id)).data
        )


class AgentDisableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, agent_id):
        agent = get_object_or_404(Agent, pk=agent_id)
        agent.status = Agent.Status.DISABLED
        agent.save(update_fields=["status"])
        return envelope({"agent_id": agent_id, "status": agent.status})


class AgentContextView(APIView):
    authentication_classes = []
    permission_classes = [ToolTokenPermission]

    def get(self, request, agent_id):
        agent = get_object_or_404(Agent.objects.select_related("dataset"), pk=agent_id)
        latest = Checkin.objects.filter(agent=agent).select_related("spot").first()
        chunks = agent.dataset.chunks.all()[:10] if agent.dataset else []
        return envelope({
            "agent_id": agent.agent_id,
            "name": agent.name,
            "personality_prompt": agent.personality_prompt,
            "voice_id": agent.voice_id,
            "knowledge_references": agent.knowledge_references,
            "tool_endpoint_url": agent.tool_endpoint_url,
            "config_version": agent.config_version,
            "prompt_version": agent.prompt_version,
            "official_sync_status": agent.official_sync_status,
            "current_spot": {"spot_id": latest.spot_id, "name": latest.spot.name} if latest else None,
            "last_checkin_at": latest.checked_in_at if latest else None,
            "knowledge_summary": [{"title": chunk.title, "summary": chunk.summary, "source_ref": chunk.source_ref} for chunk in chunks],
        })
