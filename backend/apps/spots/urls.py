from django.urls import path
from .views import SpotDetailView, SpotDisableView, SpotListView

urlpatterns = [path("spots", SpotListView.as_view()), path("spots/<str:spot_id>", SpotDetailView.as_view()), path("spots/<str:spot_id>/disable", SpotDisableView.as_view())]
