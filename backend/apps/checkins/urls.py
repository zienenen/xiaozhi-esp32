from django.urls import path
from .views import CheckinDetailView, CheckinListView, LocationEventsView

urlpatterns = [path("location-events", LocationEventsView.as_view()), path("checkins", CheckinListView.as_view()), path("checkins/<str:checkin_id>", CheckinDetailView.as_view())]
