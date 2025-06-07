from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from Documents.models import Document
from users.models import CustomUser


@shared_task
def send_email_about_create_document(user_email=None):
    """
    Sending email about a creating document
    """

    admin = CustomUser.objects.get(email="nurlan.grachyov@mail.ru")

    if user_email:
        users = [admin.email, user_email]
        send_mail(
            "Новый документ создан",
            "Создан новый документ.",
            EMAIL_HOST_USER,
            users,
        )
    else:
        raise ValueError("Требуется аргумент user_email.")


@shared_task
def send_email_about_update_document(document_id=None):
    """
    Sending about an updating document
    """

    if document_id:
        document = Document.objects.get(id=document_id)
        users = [document.owner.email]
        if document.status == "Подтвержден":
            send_mail(
                "Документ обновлён",
                "Ваш документ подтверждён.",
                EMAIL_HOST_USER,
                users,
            )
        elif document.status == "Отклонён":
            send_mail(
                "Документ обновлён",
                "Ваш документ отклонён.",
                EMAIL_HOST_USER,
                users,
            )
    else:
        raise ValueError("Требуется аргумент document_id.")


@shared_task
def send_email_about_new_comment(document_id=None, document_owner=None):
    """
    Sending about a creating comment
    """

    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist as exc:
        raise ValueError("Такой документ не найден") from exc

    if not document_owner or not isinstance(document_owner, str):
        raise ValueError("Неверный email владельца документа.")

    subject = f"Новый комментарий к документу '{document.title}'"
    message = (
        f"Появился новый комментарий к документу:\n\nНазвание документа: {document.title}\n"
        f"Статус документа: {document.status}"
    )
    recipients = [document_owner]

    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=recipients,
    )
