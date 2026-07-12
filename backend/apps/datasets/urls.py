from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView


class DatasetsView(APIView):
    def get(self, request):
        return Response({"success": True, "data": {"module": "datasets", "todo": "list datasets"}, "error": None})


class KnowledgeSearchView(APIView):
    def post(self, request):
        return Response({"success": True, "data": {"module": "datasets", "todo": "search scenic knowledge"}, "error": None})


urlpatterns = [
    path("datasets", DatasetsView.as_view(), name="datasets"),
    path("knowledge/search", KnowledgeSearchView.as_view(), name="knowledge-search"),
]
