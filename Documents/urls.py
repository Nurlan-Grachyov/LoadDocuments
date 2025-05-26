from django.urls import path

from Documents.apps import DocumentsConfig
from Documents.views import DocumentListCreateApiView, DocumentRetrieveUpdateAPIView

app_name = DocumentsConfig.name

urlpatterns = [
    path(
        "list_create_documents/",
        DocumentListCreateApiView.as_view(),
        name="list_create_documents",
    ),
    path(
        "retrieve_update_documents/",
        DocumentRetrieveUpdateAPIView.as_view(),
        name="retrieve_update_documents",
    )
]