from django.db import models


class Dataset(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"
        CHUNKED = "chunked"
        VECTORIZED = "vectorized"
        FAILED = "failed"
        DISABLED = "disabled"

    dataset_id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=20, default="document")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    failure_reason = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def public_status(self):
        return "ready" if self.status in {self.Status.CHUNKED, self.Status.VECTORIZED} else self.status


class DatasetChunk(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="chunks")
    title = models.CharField(max_length=200)
    summary = models.TextField()
    source_ref = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.dataset_id}: {self.title}"
