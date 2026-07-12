from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView


class SpotsView(APIView):
    def get(self, request):
        return Response({"success": True, "data": {"module": "spots", "todo": "list spots"}, "error": None})


urlpatterns = [
    path("spots", SpotsView.as_view(), name="spots"),
]
