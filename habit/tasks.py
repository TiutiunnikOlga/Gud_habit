import os

import requests
from celery import shared_task
from dotenv import load_dotenv

from habit.models import Habit

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = os.getenv("TELEGRAM_API_URL")


@shared_task
def send_habit_reminder():
    habits = Habit.objects.select_related("user").all()
    for habit in habits:
        if not habit.user.telegram_id:
            continue

        message = (
            f"Напоминание!\n"
            f"Привычка: *{habit.action}*\n"
            f"Место: {habit.place}\n"
            f"Время: {habit.time}\n"
            f'{"(Полезная)" if not habit.is_pleasant else "(Приятная)"}'
        )
        requests.post(
            TELEGRAM_API_URL,
            data={
                "chat_id": habit.user.telegram_id,
                "text": message,
                "parse_mode": "Markdown",
            },
        )
