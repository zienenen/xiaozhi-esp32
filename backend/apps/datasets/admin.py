from django.contrib import admin
from .models import Dataset, DatasetChunk

class DatasetChunkInline(admin.TabularInline):
    model = DatasetChunk
    extra = 0

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("dataset_id", "name", "status", "updated_at")
    inlines = (DatasetChunkInline,)
