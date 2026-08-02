from django.contrib import admin

from .models import ConversationMessage, ConversationSession, OfficialSyncLog


class ConversationMessageInline(admin.TabularInline):
    model = ConversationMessage
    extra = 0


@admin.register(ConversationSession)
class ConversationSessionAdmin(admin.ModelAdmin):
    list_display = ("session_id", "device", "agent", "spot", "source", "status", "started_at")
    list_filter = ("source", "status")
    search_fields = ("session_id", "device__device_id", "agent__agent_id", "summary")
    inlines = [ConversationMessageInline]


@admin.register(OfficialSyncLog)
class OfficialSyncLogAdmin(admin.ModelAdmin):
    list_display = ("sync_id", "target_type", "target_id", "status", "operator", "created_at", "synced_at")
    list_filter = ("target_type", "status", "sync_mode")
    search_fields = ("sync_id", "target_id", "operator", "note", "failure_reason")

