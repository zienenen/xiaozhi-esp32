from django.urls import path

from .views import (
    ConversationSessionDetailView, ConversationSessionListView,
    DeviceConversationEventView, OfficialSyncLogDetailView, OfficialSyncLogListView,
)

urlpatterns = [
    path("conversation-sessions", ConversationSessionListView.as_view()),
    path("conversation-sessions/<str:session_id>", ConversationSessionDetailView.as_view()),
    path("device-conversation-events", DeviceConversationEventView.as_view()),
    path("official-sync-logs", OfficialSyncLogListView.as_view()),
    path("official-sync-logs/<str:sync_id>", OfficialSyncLogDetailView.as_view()),
]
