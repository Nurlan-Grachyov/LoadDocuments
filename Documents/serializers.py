from rest_framework import serializers

from Documents.models import Document, Comments


class DocumentsSerializer(serializers.ModelSerializer):
    """
    Serializer for a document
    """

    class Meta:
        model = Document
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    """
    Serializer for a comment
    """

    class Meta:
        model = Comments
        fields = "__all__"
