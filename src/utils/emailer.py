from email.message import EmailMessage

import aiosmtplib

from src.configs import settings


async def send_email(sender: str, recipients: list, subject: str, content: str):
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipients
    message["Subject"] = subject
    message.set_content(content)

    await aiosmtplib.send(
        message,
        sender=sender,
        recipients=recipients,
        hostname=settings.emailer.host,
        port=settings.emailer.port,
    )
