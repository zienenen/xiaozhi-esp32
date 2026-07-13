from django.db import models


class Agent(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        DISABLED = "disabled"
        DRAFT = "draft"

    agent_id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=120)
    personality_prompt = models.TextField()
    voice_id = models.CharField(max_length=120, blank=True)
    dataset = models.ForeignKey("datasets.Dataset", null=True, blank=True, on_delete=models.SET_NULL, related_name="agents")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    series = models.CharField(max_length=120, blank=True)
    rarity = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.name
