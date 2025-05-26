from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from Documents.models import Document
from Documents.permissions import Moderators, IsSuperUser
from Documents.serializers import DocumentsSerializer


class DocumentListCreateApiView(generics.ListCreateAPIView):
    """
    The view for creating and viewing a list of documents
    """

    serializer_class = DocumentsSerializer
    queryset = Document.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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