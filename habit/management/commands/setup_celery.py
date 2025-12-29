from django.core.management import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = 'Setup Celery Beat periodic tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pool',
            type=str,
            default='solo',
            help='Тип пула воркеров (по умолчанию: solo)'
        )
        parser.add_argument(
            '--loglevel',
            type=str,
            default='INFO',
            help='Уровень логирования (по умолчанию: INFO)'
        )

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS
        )

        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Send habit reminders every hour',
            task='habit.tasks.send_habit_reminder'
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Celery task')
            )
        else:
            self.stdout.write('Celery task already exists')