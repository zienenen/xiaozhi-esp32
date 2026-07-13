from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config.api import ToolTokenPermission, api_error, envelope
from .models import Dataset, DatasetChunk
from .serializers import ChunkSerializer, DatasetSerializer


class DatasetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return envelope(DatasetSerializer(Dataset.objects.prefetch_related("chunks", "agents", "spots"), many=True).data)


class DatasetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        return envelope(DatasetSerializer(get_object_or_404(Dataset, pk=dataset_id)).data)


class DatasetChunksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, pk=dataset_id)
        return envelope(ChunkSerializer(dataset.chunks.all(), many=True).data)


class KnowledgeSearchView(APIView):
    authentication_classes = []
    permission_classes = [ToolTokenPermission]

    def post(self, request):
        query = str(request.data.get("query", "")).strip()
        if not query:
            return api_error("query_required", "查询内容不能为空")
        rows = DatasetChunk.objects.select_related("dataset").filter(Q(title__icontains=query) | Q(summary__icontains=query))
        if request.data.get("dataset_id"):
            rows = rows.filter(dataset_id=request.data["dataset_id"])
        limit = min(max(int(request.data.get("limit", 5)), 1), 20)
        return envelope({"query": query, "results": [{"dataset_id": row.dataset_id, "title": row.title, "summary": row.summary, "source_ref": row.source_ref} for row in rows[:limit]]})
