from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import User
from habit.models import Habit


class HabitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_duration_limit(self):
        habit = Habit(
            user=self.user, place="Дом", time="12:00:00", action="Тест", duration=121
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn(
            "Время выполнения не должно превышать 120 секунд", str(cm.exception)
        )

    def test_reward_and_related_habit_exclusive(self):
        related = Habit.objects.create(
            user=self.user,
            is_pleasant=True,
            place="Дом",
            time="12:00:00",
            action="Связанная",
            duration=60,
        )
        habit = Habit(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Тест",
            reward="Награда",
            related_habit=related,
            duration=60,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn(
            "Нельзя указывать вознаграждение и связанную привычку одновременно",
            str(cm.exception),
        )

    def test_pleasant_habit_no_reward_or_related(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Тест",
            is_pleasant=True,
            reward="Награда",
            duration=60,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn(
            "Приятная привычка не может иметь связанную привычку или вознаграждение",
            str(cm.exception),
        )

    def test_related_habit_must_be_pleasant(self):
        unpleasant = Habit.objects.create(
            user=self.user,
            is_pleasant=False,
            place="Дом",
            time="12:00:00",
            action="Неприятная",
            duration=60,
        )
        habit = Habit(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Тест",
            related_habit=unpleasant,
            duration=60,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn("Связанная привычка должна быть приятной", str(cm.exception))

    def test_frequency_limit(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Тест",
            frequency=8,
            duration=60,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn(
            "Привычку нельзя выполнять реже чем раз в 7 дней", str(cm.exception)
        )

    def test_valid_habit_saves(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Читать",
            duration=90,
            frequency=5,
        )
        try:
            habit.full_clean()
            habit.save()
        except ValidationError:
            self.fail("Корректная привычка не должна вызывать ValidationError")
        self.assertEqual(Habit.objects.count(), 1)

    def test_str_method(self):
        habit = Habit.objects.create(
            user=self.user, action="Тест", time="10:00:00", place="Офис", duration=60
        )
        expected = f"{self.user.email}: Тест в 10:00:00 в Офис"
        self.assertEqual(str(habit), expected)
