from django.contrib import admin

from Documents.models import Document

class DocumentAdmin(admin.ModelAdmin):
      def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.groups.filter(name='Moderators').exists():
            fields.remove('status')
        return fields

admin.site.register(Document, DocumentAdmin)