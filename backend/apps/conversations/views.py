from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.devices.authentication import authenticate_device
from apps.devices.models import DeviceBinding
from config.api import api_error
from config.api import envelope
from .models import ConversationMessage, ConversationSession, OfficialSyncLog
from .serializers import (
    ConversationSessionSerializer, ConversationSessionWriteSerializer, DeviceConversationEventSerializer,
    OfficialSyncLogSerializer,
)


class ConversationSessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = ConversationSession.objects.select_related("device", "agent", "spot").prefetch_related("messages")
        for key in ("device_id", "agent_id", "spot_id", "source", "status"):
            if request.query_params.get(key):
                rows = rows.filter(**{key: request.query_params[key]})
        if request.query_params.get("date_from"):
            rows = rows.filter(started_at__gte=request.query_params["date_from"])
        if request.query_params.get("date_to"):
            rows = rows.filter(started_at__lte=request.query_params["date_to"])
        return envelope(ConversationSessionSerializer(rows, many=True).data)

    def post(self, request):
        serializer = ConversationSessionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()
        return envelope(ConversationSessionSerializer(session).data, status=201)


class ConversationSessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        row = get_object_or_404(
            ConversationSession.objects.select_related("device", "agent", "spot").prefetch_related("messages"),
            pk=session_id,
        )
        return envelope(ConversationSessionSerializer(row).data)


class DeviceConversationEventView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        device, error = authenticate_device(request)
        if error:
            return error
        try:
            agent = device.binding.agent
        except DeviceBinding.DoesNotExist:
            return api_error("device_not_bound", "Device is not bound to an agent.")

        serializer = DeviceConversationEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        event_metadata = {
            **data["metadata"],
            "official_session_id": data["official_session_id"],
            "event_source": data["content_source"],
            "session_source": data["session_source"],
        }
        reported_agent_id = data.get("agent_id")
        if reported_agent_id:
            event_metadata["reported_agent_id"] = reported_agent_id
            event_metadata["agent_binding_overridden"] = reported_agent_id != agent.agent_id

        with transaction.atomic():
            session, created = ConversationSession.objects.get_or_create(
                device=device,
                official_session_id=data["official_session_id"],
                defaults={
                    "agent": agent,
                    "spot": data.get("spot"),
                    "source": ConversationSession.Source.DEVICE_LOG,
                    "started_at": data["created_at"],
                    "status": ConversationSession.Status.OPEN,
                },
            )
            if session.spot_id is None and data.get("spot") is not None:
                session.spot = data["spot"]
                session.save(update_fields=["spot"])
            message = ConversationMessage.objects.create(
                session=session,
                role=data["role"],
                content=data["content"],
                content_source=ConversationMessage.ContentSource.DEVICE_LOG,
                created_at=data["created_at"],
                metadata=event_metadata,
            )

        return envelope({
            "accepted": True,
            "session_created": created,
            "session_id": session.session_id,
            "official_session_id": session.official_session_id,
            "message_id": message.message_id,
            "device_id": device.device_id,
            "agent_id": session.agent_id,
            "role": message.role,
            "created_at": message.created_at,
        }, status=201 if created else 200)


class OfficialSyncLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = OfficialSyncLog.objects.all()
        for key in ("target_type", "target_id", "status", "sync_mode"):
            if request.query_params.get(key):
                rows = rows.filter(**{key: request.query_params[key]})
        return envelope(OfficialSyncLogSerializer(rows, many=True).data)

    def post(self, request):
        payload = request.data.copy()
        payload.setdefault("operator", request.user.get_username())
        serializer = OfficialSyncLogSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        row = serializer.save()
        return envelope(OfficialSyncLogSerializer(row).data, status=201)


class OfficialSyncLogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, sync_id):
        return envelope(OfficialSyncLogSerializer(get_object_or_404(OfficialSyncLog, pk=sync_id)).data)

    def patch(self, request, sync_id):
        row = get_object_or_404(OfficialSyncLog, pk=sync_id)
        serializer = OfficialSyncLogSerializer(row, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        row = serializer.save()
        return envelope(OfficialSyncLogSerializer(row).data)
