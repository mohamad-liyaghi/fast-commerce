from fastapi_mail import FastMail, ConnectionConfig
from fastapi.templating import Jinja2Templates
from .base import settings

template_path = Jinja2Templates(directory="src/templates/email")
configs = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=int(settings.MAIL_PORT),
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

mail = FastMail(configs)
