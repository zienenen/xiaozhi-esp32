from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"success": True, "data": {"status": "ok"}, "error": None})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health", HealthView.as_view(), name="health"),
    path("api/v1/", include("apps.devices.urls")),
    path("api/v1/", include("apps.agents.urls")),
    path("api/v1/", include("apps.spots.urls")),
    path("api/v1/", include("apps.nfc_tags.urls")),
    path("api/v1/", include("apps.checkins.urls")),
    path("api/v1/", include("apps.datasets.urls")),
    path("api/v1/", include("apps.conversations.urls")),
    path("api/v1/", include("apps.demo.urls")),
]
