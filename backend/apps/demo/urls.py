from django.urls import path
from .views import DemoOverviewView, SimulateCheckinView

urlpatterns = [path("demo/overview", DemoOverviewView.as_view()), path("demo/simulate-checkin", SimulateCheckinView.as_view())]
