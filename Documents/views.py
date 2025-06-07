from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Documents.models import Document, Comments
from Documents.permissions import IsModerators, IsSuperUser
from Documents.serializers import DocumentsSerializer, CommentsSerializer

from .tasks import send_email_about_create_document, send_email_about_update_document


class DocumentListCreateApiView(generics.ListCreateAPIView):
    """
    The view for creating and viewing a list of documents
    """

    serializer_class = DocumentsSerializer
    queryset = Document.objects.all()

    def perform_create(self, serializer):
        """
        Method for saving a document and sending a notification when it is created
        """

        document = serializer.save(owner=self.request.user)
        send_email_about_create_document.delay(None, document.owner.email)
        return Response({"message": "Документ успешно создан"}, status=201)

    def get_permissions(self):
        """
        Method of providing access rights
        """

        if self.request.method in ("GET", "POST"):
            permission_classes = [IsModerators]
        else:
            return False
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        The return method of product list by criteria
        """

        if (
                self.request.user.groups.filter(name="Moderators").exists()
                or self.request.user.is_superuser
        ):
            return Document.objects.all()
        return Document.objects.filter(owner=self.request.user)


class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Method for reading, updating and deleting a document
    """

    serializer_class = DocumentsSerializer
    queryset = Document.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()

        send_email_about_update_document.delay(instance.id)

        return Response({'message': 'Документ успешно обновлен'}, status=200)

    def get_permissions(self):
        """
        Method of granting access rights.
        """

        if self.request.method in ("PUT", "PATCH", "GET"):
            permission_classes = [IsModerators]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]


# class CommentViewSet(viewsets.ModelViewSet):
#     """
#     Method for reading, updating and deleting a comment
#     """
#
#     serializer_class = CommentsSerializer
#     queryset = Comments.objects.all()
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         """
#         The creating method of a comment
#         """
#
#         comment = serializer.save(owner=self.request.user)
#         send_email_about_new_comment.delay(None, comment.document.owner.email)
#         return Response({"message": "Документ успешно создан"}, status=201)
