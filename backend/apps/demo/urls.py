from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView


class DemoOverviewView(APIView):
    def get(self, request):
        return Response({"success": True, "data": {"module": "demo", "todo": "overview"}, "error": None})


class SimulateCheckinView(APIView):
    def post(self, request):
        return Response({"success": True, "data": {"module": "demo", "todo": "simulate check-in"}, "error": None})


urlpatterns = [
    path("demo/overview", DemoOverviewView.as_view(), name="demo-overview"),
    path("demo/simulate-checkin", SimulateCheckinView.as_view(), name="simulate-checkin"),
]
