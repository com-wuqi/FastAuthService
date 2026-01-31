from fastapi_mail import MessageSchema, MessageType
from typing import List
from ..depends import get_logger,mail
import asyncio

logger = get_logger(__name__)


class EmailService:
    def __init__(self):
        pass

    @staticmethod
    async def send_common_email(
            subject: str, recipients: List[str],
            body: str, subtype: MessageType = MessageType.plain
    ) -> bool:
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=subtype
        )
        try:
            await mail.send_message(message)
            return True
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    async def send_html_email(
            subject: str, recipients: List[str],
            html_body: str
    ) -> bool:
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=html_body,
            subtype=MessageType.html
        )
        try:
            await mail.send_message(message)
            return True
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    async def send_verify_email(
            email: str,
            code: str
    ) -> bool:
        html_body = f"""
        <html>
        <body>
        <p> code : <strong>{code}</strong> </p>
        </body>
        </html>
        """
        messages = MessageSchema(
            subject="Verify your email",
            recipients=[email],
            body=html_body,
            subtype=MessageType.html
        )
        try:
            await mail.send_message(messages)
            return True
        except Exception as e:
            logger.error(e)
            return False
