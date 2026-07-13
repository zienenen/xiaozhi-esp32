from django.urls import path
from .views import AgentContextView, AgentDetailView, AgentDisableView, AgentListView

urlpatterns = [
    path("agents", AgentListView.as_view()),
    path("agents/<str:agent_id>", AgentDetailView.as_view()),
    path("agents/<str:agent_id>/disable", AgentDisableView.as_view()),
    path("agents/<str:agent_id>/context", AgentContextView.as_view()),
]
