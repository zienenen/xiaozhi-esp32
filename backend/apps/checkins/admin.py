from django.contrib import admin
from .models import Checkin

@admin.register(Checkin)
class CheckinAdmin(admin.ModelAdmin):
    list_display = ("checkin_id", "device", "spot", "result", "source", "checked_in_at")
    list_filter = ("result", "source", "spot")
