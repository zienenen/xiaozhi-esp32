from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.checkins.models import Checkin
from config.api import ToolTokenPermission, envelope
from .models import Agent
from .serializers import AgentSerializer


class AgentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return envelope(AgentSerializer(Agent.objects.all(), many=True).data)

    def post(self, request):
        serializer = AgentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return envelope(serializer.data, status=201)


class AgentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, agent_id):
        return envelope(AgentSerializer(get_object_or_404(Agent, pk=agent_id)).data)

    def patch(self, request, agent_id):
        serializer = AgentSerializer(get_object_or_404(Agent, pk=agent_id), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return envelope(serializer.data)


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
            "current_spot": {"spot_id": latest.spot_id, "name": latest.spot.name} if latest else None,
            "last_checkin_at": latest.checked_in_at if latest else None,
            "knowledge_summary": [{"title": chunk.title, "summary": chunk.summary, "source_ref": chunk.source_ref} for chunk in chunks],
        })
