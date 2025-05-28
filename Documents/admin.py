from django.contrib import admin

from Documents.models import Document


class DocumentAdmin(admin.ModelAdmin):
    """
    This customization ensures that only moderators can see or edit the 'status' field.
    If the current user does not belong to the group named 'Moderators',
    the 'status' field will be removed from the form.
    """

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.groups.filter(name="Moderators").exists():
            fields.remove("status")
        return fields


admin.site.register(Document, DocumentAdmin)
