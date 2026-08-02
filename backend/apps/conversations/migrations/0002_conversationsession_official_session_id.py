from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("conversations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversationsession",
            name="official_session_id",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddConstraint(
            model_name="conversationsession",
            constraint=models.UniqueConstraint(
                fields=("device", "official_session_id"),
                name="unique_device_official_conversation_session",
            ),
        ),
    ]
