import asyncio
from celery import shared_task
from src.core.email import base_send_email


@shared_task
def send_email(
        subject: str,
        to_email: str,
        body: dict,
        template_name: str = None
) -> str:
    """
    Send email to user (In background)
    :param subject: Subject of email
    :param to_email: Email address of user
    :param body: Body of email
    :param template_name: Name of template
    :return:
    """
    asyncio.run(base_send_email(
        subject=subject,
        to_email=to_email,
        body=body,
        template_name=template_name
    ))
    return f"Email sent to {to_email}"
