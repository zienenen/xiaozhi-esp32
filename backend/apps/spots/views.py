from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config.api import envelope
from .models import ScenicSpot
from .serializers import ScenicSpotSerializer


class SpotListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return envelope(ScenicSpotSerializer(ScenicSpot.objects.all(), many=True).data)

    def post(self, request):
        serializer = ScenicSpotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return envelope(serializer.data, status=201)


class SpotDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, spot_id):
        return envelope(ScenicSpotSerializer(get_object_or_404(ScenicSpot, pk=spot_id)).data)

    def patch(self, request, spot_id):
        serializer = ScenicSpotSerializer(get_object_or_404(ScenicSpot, pk=spot_id), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return envelope(serializer.data)


class SpotDisableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, spot_id):
        spot = get_object_or_404(ScenicSpot, pk=spot_id)
        spot.status = ScenicSpot.Status.DISABLED
        spot.save(update_fields=["status"])
        return envelope({"spot_id": spot_id, "status": spot.status})
