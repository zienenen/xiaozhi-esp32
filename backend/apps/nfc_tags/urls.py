from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView


class NfcTagsView(APIView):
    def get(self, request):
        return Response({"success": True, "data": {"module": "nfc_tags", "todo": "list nfc tags"}, "error": None})


urlpatterns = [
    path("nfc-tags", NfcTagsView.as_view(), name="nfc-tags"),
]
