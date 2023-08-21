import asyncio
from celery import shared_task
from fastapi_mail import MessageSchema, MessageType
from src.core.configs import mail, template_path


async def _send_email(
        subject: str,
        to_email: str,
        body: dict,
        template_name: str = None
) -> None:
    """
    Base function for sending email to user.
    :param subject: Subject of email
    :param to_email: Email address of user
    :param body: Body of email
    :param template_name: Name of template
    """
    html_content = template_path.TemplateResponse(
        template_name, {"request": None, **body}
    ).body

    # Send email
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=html_content,
        subtype=MessageType.html
    )

    await mail.send_message(message)


@shared_task
def send_email(
        subject: str,
        to_email: str,
        body: dict,
        template_name: str = None
) -> str:
    """
    Send email to user (In background)
    """
    asyncio.run(_send_email(
        subject=subject,
        to_email=to_email,
        body=body,
        template_name=template_name
    ))
    return f"Email sent to {to_email}"
