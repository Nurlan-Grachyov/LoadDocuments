from django.urls import path
from rest_framework.routers import DefaultRouter

from Documents.apps import DocumentsConfig
from Documents.views import (DocumentListCreateApiView,
                             DocumentRetrieveUpdateDestroyAPIView, CommentViewSet)

app_name = DocumentsConfig.name
router = DefaultRouter()
router.register(r'^(?P<document_pk>\d+)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    path(
        "list_create_documents/",
        DocumentListCreateApiView.as_view(),
        name="list_create_documents",
    ),
    path(
        "retrieve_update_delete_documents/<int:pk>/",
        DocumentRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve_update_delete_documents",
    ),
] + router.urls
