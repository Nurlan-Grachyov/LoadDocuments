from celery import shared_task
from django.core.mail import send_mail

from Documents.models import Document
from config.settings import EMAIL_HOST_USER
from users.models import CustomUser

@shared_task
def send_email_about_update_document(document_id=None, user_email=None):
    """Отправляет уведомление о документе."""
    print("good")
    admin = CustomUser.objects.get(email="nurlan.grachyov@mail.ru")

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
    elif user_email:
        print(user_email)
        users = [admin.email, user_email]
        send_mail(
            "Новый документ создан",
            "Создан новый документ.",
            EMAIL_HOST_USER,
            users,
        )
    else:
        raise ValueError("Требуется хотя бы один аргумент: document_id или user_email.")