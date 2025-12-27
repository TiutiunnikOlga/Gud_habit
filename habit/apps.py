from django.apps import AppConfig


class HabitConfig(AppConfig):
    name = "habit"

    def ready(self):

        from django_celery_beat.models import IntervalSchedule, PeriodicTask

        shedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
        PeriodicTask.objects.get_or_create(
            interval=shedule,
            name="Send habit reminders every hour",
            task="habit.tasks.send_habit_reminder",
        )
