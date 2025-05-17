from flask_mail import Message
from . import mail


def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients)
    msg.html = body
    mail.send(msg)
