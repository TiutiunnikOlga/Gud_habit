from django.apps import AppConfig


class HabitConfig(AppConfig):
    name = "habit"

    def ready(self):
        from django.db import connection
        from django.apps import apps

        if not apps.ready:
            return

        table_names = connection.introspection.table_names()

        required_tables = [
            'django_celery_beat_intervalschedule',
            'django_celery_beat_periodictask'
        ]

        if all(table in table_names for table in required_tables):

            from django_celery_beat.models import IntervalSchedule, PeriodicTask

            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.HOURS,
            )

            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name="Send habit reminders every hour",
                task="habit.tasks.send_habit_reminder",
            )
        else:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(
                "Celery Beat tables not found. Skipping periodic task setup "
                "(likely during migrations)."
            )

