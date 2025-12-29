from .celery import app as celery_app

default_app_config = "habit.apps.HabitConfig"

__all__ = ("celery_app",)
