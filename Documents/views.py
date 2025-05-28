from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Documents.models import Document
from Documents.permissions import Moderators, IsSuperUser
from Documents.serializers import DocumentsSerializer
from users.models import CustomUser

from .tasks import send_email_about_update_document

class DocumentListCreateApiView(generics.ListCreateAPIView):
    """
    The view for creating and viewing a list of documents
    """

    serializer_class = DocumentsSerializer
    queryset = Document.objects.all()

    def perform_create(self, serializer):
        """ Метод для сохранения документа и отправки уведомления о его создании. """
        document = serializer.save(owner=self.request.user)
        print(self.request.user)
        send_email_about_update_document.delay(None, document.owner.email)
        return Response({"message": "Документ успешно создан"}, status=201)

    def get_permissions(self):
        """
        Метод предоставления прав доступа.
        """

        if self.request.method in ("GET", "POST"):
            print("4")
            permission_classes = [Moderators]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        The return method of product list by criteria
        """
        print("5")
        if (
            self.request.user.groups.filter(name="Moderators").exists()
            or self.request.user.is_superuser
        ):
            return Document.objects.all()
        print("6")
        return Document.objects.filter(owner=self.request.user)


class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentsSerializer
    queryset = Document.objects.all()

    def partial_update(self, request, *args, **kwargs):
        document_id = kwargs.get("pk")
        print(document_id)
        try:
            document = Document.objects.get(id=document_id)
            print(document)
        except Document.DoesNotExist:
            return Response(
                {"message": "Такого документа не существует"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DocumentsSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            print("ser.is_valid")
            serializer.save()
            print("ser2")
            send_email_about_update_document.delay(document_id, None)
            return Response({"message": "Документ успешно обновлен"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """
        Method of granting access rights.
        """

        if self.request.method in ("PUT", "PATCH",):
            print("1")
            permission_classes = [Moderators]
        elif self.request.method == "DELETE":
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]