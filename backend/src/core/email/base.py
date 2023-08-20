from fastapi_mail import MessageSchema, MessageType
from src.core.config import settings
from .config import mail, template_path


async def base_send_email(
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

    if settings.env.get('TESTING') == '1':
        return

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
