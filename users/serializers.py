from rest_framework import serializers

from users.models import CustomUser, Payments


class RegisterSerializer(serializers.ModelSerializer):
    """
    The serializer of a registration with the method of a creating
    """

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        """
        The account creation method
        """

        user = CustomUser(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()
        return user


class PaymentsSerializer(serializers.ModelSerializer):
    """
    The payments serializer
    """

    class Meta:
        model = Payments
        fields = "__all__"
