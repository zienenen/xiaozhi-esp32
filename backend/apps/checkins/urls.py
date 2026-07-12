from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView


class LocationEventsView(APIView):
    def post(self, request):
        return Response({"success": True, "data": {"module": "checkins", "todo": "location summary accepted"}, "error": None})


class CheckinsView(APIView):
    def get(self, request):
        return Response({"success": True, "data": {"module": "checkins", "todo": "list check-ins"}, "error": None})

    def post(self, request):
        return Response({"success": True, "data": {"module": "checkins", "todo": "check-in accepted"}, "error": None})


urlpatterns = [
    path("location-events", LocationEventsView.as_view(), name="location-events"),
    path("checkins", CheckinsView.as_view(), name="checkins"),
]
