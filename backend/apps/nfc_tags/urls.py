from django.urls import path
from .views import NfcTagDetailView, NfcTagDisableView, NfcTagListView

urlpatterns = [path("nfc-tags", NfcTagListView.as_view()), path("nfc-tags/<str:tag_id>", NfcTagDetailView.as_view()), path("nfc-tags/<str:tag_id>/disable", NfcTagDisableView.as_view())]
