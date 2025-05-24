from rest_framework import serializers

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации с методом создания
    """

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        """
        Метод создания аккаунта
        """

        user = CustomUser(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()
        return user