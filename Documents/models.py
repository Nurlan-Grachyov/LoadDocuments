from django.db import models


class Document(models.Model):
    """
    Модель документа
    """

    PENDING = "Ожидает одобрения"
    APPROVED = "Подтвержден"
    REJECTED = "Отклонён"

    STATUS_CHOICES = [
        (PENDING, "Ожидает одобрения"),
        (APPROVED, "Подтвержден"),
        (REJECTED, "Отклонён")
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")
    status = models.CharField(
        max_length=17,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    def __str__(self):
        return self.title