from rest_framework import serializers

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, attrs):
        duration = attrs.get("duration")
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")
        is_pleasant = attrs.get("is_pleasant", False)

        if duration and duration > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд"
            )
        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку"
            )
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь вознаграждение или связанную привычку"
            )
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной")

        frequency = attrs.get("frequency", 1)
        if frequency > 7:
            raise serializers.ValidationError(
                "Привычку нельзя выполнять реже чем раз в 7 дней"
            )

        return attrs
