from . import celery_app
from .email_utils import send_email


@celery_app.task(name="send_email_task")
def send_email_task(subject, recipients, body):
    send_email(subject, recipients, body)
    return f"send email {subject} to {recipients}"
