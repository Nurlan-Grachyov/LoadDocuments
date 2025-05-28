from django.db import models
from django.db.models import ForeignKey

from config.settings import AUTH_USER_MODEL


class Document(models.Model):
    """
    The model for a document
    """

    PENDING = "Ожидает одобрения"
    APPROVED = "Подтвержден"
    REJECTED = "Отклонён"

    STATUS_CHOICES = [
        (PENDING, "Ожидает одобрения"),
        (APPROVED, "Подтвержден"),
        (REJECTED, "Отклонён"),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")
    status = models.CharField(
        max_length=17, choices=STATUS_CHOICES, default=PENDING, blank=True
    )
    owner = ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="Documents",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title
