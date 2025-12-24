from django.test import TestCase
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class UserManagerTest(TestCase):
    def test_create_user(self):
        """Проверка создания обычного пользователя"""
        user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        """Проверка, что создание пользователя без email вызывает ошибку"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpass123")

    def test_create_superuser(self):
        """Проверка создания суперпользователя"""
        admin = User.objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_sets_flags_correctly(self):
        """Проверка, что is_staff и is_superuser установлены по умолчанию"""
        admin = User.objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class UserModelTest(TestCase):
    def test_user_string_representation(self):
        """Проверка строкового представления пользователя"""
        user = User(email="test@example.com")
        self.assertEqual(str(user), "test@example.com")

    def test_user_meta_verbose_names(self):
        """Проверка verbose_name и verbose_name_plural"""
        self.assertEqual(User._meta.verbose_name, "Пользователь")
        self.assertEqual(User._meta.verbose_name_plural, "Пользователи")


class UserReadyMethodTest(TestCase):
    def test_ready_creates_periodic_task(self):
        """Проверка, что метод ready создаёт периодическую задачу"""
        # Вызываем логику из ready()
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=24, period=IntervalSchedule.HOURS
        )
        task_name = "Block users"
        PeriodicTask.objects.create(
            interval=schedule,
            name=task_name,
            task="users.tasks.block_inactive_users",
            args=json.dumps(["arg1", "arg2"]),
            kwargs=json.dumps({"be_careful": True}),
            expires=timezone.now() + timedelta(seconds=30),
        )

        # Проверяем, что задача создалась
        task = PeriodicTask.objects.get(name=task_name)
        self.assertEqual(task.task, "users.tasks.block_inactive_users")
        self.assertEqual(json.loads(task.args), ["arg1", "arg2"])
        self.assertEqual(json.loads(task.kwargs), {"be_careful": True})
        self.assertLess(task.expires, timezone.now() + timedelta(seconds=31))
        self.assertGreater(task.expires, timezone.now())

    def test_ready_does_not_create_duplicate_tasks(self):
        """Проверка, что задача не дублируется при повторном вызове"""
        # Вызываем дважды — должно быть только одна задача с именем
        for _ in range(2):
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=24, period=IntervalSchedule.HOURS
            )
            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name="Block users",
                defaults={
                    "task": "users.tasks.block_inactive_users",
                    "args": json.dumps(["arg1", "arg2"]),
                    "kwargs": json.dumps({"be_careful": True}),
                    "expires": timezone.now() + timedelta(seconds=30),
                },
            )

        self.assertEqual(PeriodicTask.objects.filter(name="Block users").count(), 1)
