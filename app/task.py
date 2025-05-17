from . import celery_app
from .email_utils import send_email


@celery_app.task(name="send_email_task")
def send_email_task(subject, recipients, body, category):
    send_email(subject, recipients, body)
    return f"send email {category} to {recipients}"
