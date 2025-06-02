from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey

from Documents.models import Document


class CustomUser(AbstractUser):
    """
    The model for a user
    """

    username = models.CharField(null=True, blank=True, verbose_name="username")
    email = models.EmailField(unique=True, verbose_name="Email")
    is_staff = models.BooleanField(blank=True, default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email



class Payments(models.Model):
    """
    Модель платежей
    """

    CASH = "cash"
    PAYMENT_TRANSFER = "payment_transfer"

    STATUS_IN_CHOICES = [
        (CASH, "оплата наличными"),
        (PAYMENT_TRANSFER, "оплата переводом"),
    ]

    user = ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user", null=True, blank=True
    )
    pay_date = models.DateField(
        verbose_name="дата оплаты", auto_now_add=True, blank=True
    )
    paid_document = ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="paid_document",
    )

    payment_amount = models.FloatField(verbose_name="сумма оплаты")
    payment_method = models.CharField(
        choices=STATUS_IN_CHOICES, max_length=16, verbose_name="способ оплаты"
    )
    link = models.CharField(verbose_name="ссылка для оплаты", null=True, blank=True)
    session_id = models.CharField(
        verbose_name="идентификатор оплаты", null=True, blank=True
    )


    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплата"

    def __str__(self):
        return f"Вы оплатили документ {self.paid_document.title} на сумму {self.payment_amount}"
