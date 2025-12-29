from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from habit.models import Habit
from habit.serializer import HabitSerializer


class RootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "API is running"})


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Пользователь видит все свои привычки и публичные привычки других пользователей"""
        user = self.request.user
        return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        """Привязываем привычку к пользователю"""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Разрешаем просмотр публичных привычек"""
        if self.action == "list":
            return [permissions.AllowAny]
        return [permissions.IsAuthenticated]
