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
            print("Tables found. Skipping setup for now.")

        else:
            import logging
            logger = logging.getLogger(__name__)
            logger.info("Tables not found. Migration in progress.")


