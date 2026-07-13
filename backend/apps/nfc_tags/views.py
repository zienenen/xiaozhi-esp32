from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config.api import envelope
from .models import NfcTag
from .serializers import NfcTagSerializer


class NfcTagListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return envelope(NfcTagSerializer(NfcTag.objects.select_related("spot"), many=True).data)

    def post(self, request):
        serializer = NfcTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return envelope(serializer.data, status=201)


class NfcTagDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tag_id):
        return envelope(NfcTagSerializer(get_object_or_404(NfcTag, pk=tag_id)).data)

    def patch(self, request, tag_id):
        serializer = NfcTagSerializer(get_object_or_404(NfcTag, pk=tag_id), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return envelope(serializer.data)


class NfcTagDisableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tag_id):
        tag = get_object_or_404(NfcTag, pk=tag_id)
        tag.status = NfcTag.Status.DISABLED
        tag.save(update_fields=["status"])
        return envelope({"tag_id": tag_id, "status": tag.status})
