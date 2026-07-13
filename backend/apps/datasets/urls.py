from django.urls import path
from .views import DatasetChunksView, DatasetDetailView, DatasetListView, KnowledgeSearchView

urlpatterns = [path("datasets", DatasetListView.as_view()), path("datasets/<str:dataset_id>", DatasetDetailView.as_view()), path("datasets/<str:dataset_id>/chunks", DatasetChunksView.as_view()), path("knowledge/search", KnowledgeSearchView.as_view())]
