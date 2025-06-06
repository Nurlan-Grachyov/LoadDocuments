from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import Document


def approve_documents(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """
    Mass approval of documents
    """

    queryset.update(status=Document.APPROVED)
    messages.success(request, f"{queryset.count()} документов успешно одобрено.")


approve_documents.short_description = _("Одобрить выбранные документы")


def reject_documents(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """
    Mass deviation of documents
    """

    queryset.update(status=Document.REJECTED)
    messages.warning(request, f"{queryset.count()} документов отклонено.")


reject_documents.short_description = _("Отклонить выбранные документы")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Customization of the Document model administration panel.

    Main features:
    Mass approval/rejection of documents.
    Limited access to the "status" field for users outside the Moderators group.
    """

    list_display = ["title", "status"]
    search_fields = ["title"]
    ordering = ["-id"]
    actions = [approve_documents, reject_documents]

    def get_fields(self, request, obj=None):
        """Динамическое управление полем 'status'."""
        fields = super().get_fields(request, obj)

        if not request.user.groups.filter(name="Moderators").exists():
            try:
                fields.remove("status")
            except ValueError:
                pass

        return fields
