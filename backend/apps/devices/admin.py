from django.contrib import admin
from .models import BindingEvent, Device, DeviceBinding

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("device_id", "name", "online_status", "last_seen_at", "device_token_ref")
    readonly_fields = ("device_token_hash", "device_token_ref", "last_seen_at", "last_location_at")

admin.site.register(DeviceBinding)
admin.site.register(BindingEvent)
