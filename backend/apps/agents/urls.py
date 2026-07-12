from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView


class AgentContextView(APIView):
    def get(self, request, agent_id: str):
        return Response(
            {
                "success": True,
                "data": {
                    "agent_id": agent_id,
                    "module": "agents",
                    "todo": "generate agent prompt, spot context, check-in state, and knowledge summary",
                },
                "error": None,
            }
        )


urlpatterns = [
    path("agents/<str:agent_id>/context", AgentContextView.as_view(), name="agent-context"),
]
