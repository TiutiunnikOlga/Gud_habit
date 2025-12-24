from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "phone", "avatar", "telegram_id")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone"),
            avatar=validated_data.get("avatar"),
            telegram_id=validated_data.get("telegram_id"),
        )
        return user
