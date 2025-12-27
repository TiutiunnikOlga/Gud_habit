from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habit.apps import HabitConfig
from habit.views import HabitViewSet

app_name = HabitConfig.name

router = DefaultRouter()
router.register(r"habit", HabitViewSet, basename="habit")

urlpatterns = [
    path("", include(router.urls)),
]
