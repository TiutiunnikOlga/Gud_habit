import json
from datetime import timedelta

from django.apps import AppConfig
from django.utils import timezone


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        from django_celery_beat.models import IntervalSchedule, PeriodicTask

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=24, period=IntervalSchedule.HOURS
        )
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name="block users",
            task="user.tasks.block_inactive_users",
            defaults={
                "args": json.dumps(["arg1", "arg2"]),
                "kwargs": json.dumps({"be_careful": True}),
                "expires": timezone.now() + timedelta(seconds=30),
            },
        )
