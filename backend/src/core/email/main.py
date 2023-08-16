from fastapi_mail import MessageSchema, MessageType
from core.config import settings
from .config import mail, template_path


async def send_email(
        subject: str,
        to_email: str,
        body: dict,
        template_name: str = None
) -> None:
    """
    Send email to user.
    :param subject: Subject of email
    :param to_email: Email address of user
    :param body: Body of email
    :param template_name: Name of template
    :return:
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
