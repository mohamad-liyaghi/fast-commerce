from fastapi_mail import FastMail, ConnectionConfig
from fastapi.templating import Jinja2Templates
from .base import settings

template_path = Jinja2Templates(directory='src/templates/email')
configs = ConnectionConfig(
    MAIL_USERNAME=settings.env.get('MAIL_USERNAME'),
    MAIL_PASSWORD=settings.env.get('MAIL_PASSWORD'),
    MAIL_FROM=settings.env.get('MAIL_FROM'),
    MAIL_PORT=int(settings.env.get('MAIL_PORT')),
    MAIL_SERVER=settings.env.get('MAIL_SERVER'),
    MAIL_FROM_NAME=settings.env.get('MAIL_FROM_NAME'),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

mail = FastMail(configs)
