from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from Documents.models import Document
from Documents.views import (DocumentListCreateApiView,
                             DocumentRetrieveUpdateDestroyAPIView)
from users.models import CustomUser


class TestDocuments(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        moderators_group, _ = Group.objects.get_or_create(
            name="Moderators"
        )  # Модераторы получают право редактировать документы
        self.moderator = CustomUser.objects.create(email="moderator@mail.ru")
        self.moderator.set_password("12345678")
        self.moderator.groups.add(moderators_group)
        self.moderator.save()

        self.superuser = CustomUser.objects.create(email="superuser@mail.ru")
        self.superuser.set_password("12345678")
        self.superuser.is_superuser = True
        self.superuser.save()

        self.owner = CustomUser.objects.create(email="owner@mail.ru")
        self.owner.set_password("12345678")
        self.owner.save()

        self.test_file = SimpleUploadedFile("test_file.txt", b"Hello World")
        self.data_test_file = {"title": "Test Document", "file": self.test_file}

    def test_upload_document(self):
        """Test of a creating document"""


        request = self.factory.post(
            "/documents/list_create_documents/", data=self.data_test_file
        )
        force_authenticate(request, user=self.owner)
        response = DocumentListCreateApiView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Document.objects.count(), 1)
        document = Document.objects.first()
        self.assertEqual(document.title, "Test Document")

    def test_update_document(self):
        """Test of an updating document"""

        doc = Document.objects.create(title="Test Document", file=self.test_file)
        self.document = Document.objects.get(pk=doc.pk)

        new_title = "Update Test Document"
        new_file = SimpleUploadedFile("new_file.txt", b"New file content")
        self.update_data_test_file = {"title": new_title, "file": new_file}

        request = self.factory.put(
            f"/documents/retrieve_update_delete_documents/{self.document.id}/",
            data=self.update_data_test_file,
        )
        force_authenticate(request, user=self.moderator)
        response = DocumentRetrieveUpdateDestroyAPIView.as_view()(
            request, pk=self.document.id
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 1)
        updated_document = Document.objects.first()
        self.assertEqual(updated_document.title, new_title)

    def test_delete_document(self):
        """Test of a deleting document"""

        doc = Document.objects.create(title="Test Document", file=self.test_file)
        self.document = Document.objects.get(pk=doc.pk)

        request = self.factory.delete(
            f"/documents/retrieve_update_delete_documents/{self.document.id}/"
        )
        force_authenticate(request, user=self.superuser)
        response = DocumentRetrieveUpdateDestroyAPIView.as_view()(
            request, pk=self.document.id
        )

        self.document.delete()

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Document.objects.all().exists())
