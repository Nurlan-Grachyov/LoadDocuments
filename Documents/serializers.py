from rest_framework import serializers

from Documents.models import Document


class DocumentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор подписки
    """

    class Meta:
        model = Document
        fields = "__all__"