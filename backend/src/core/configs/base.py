from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "env/cache.env",
            "env/celery.env",
            "env/jwt.env",
            "env/mail.env",
            "env/pg.env",
            "env/redis.env",
        ),
    )
    POSTGRES_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str

    TEST_POSTGRES_URL: str
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str

    REDIS_URL: str
    TEST_REDIS_URL: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    CACHE_USER_KEY: str
    CACHE_USER_TTL: int
    CACHE_CART_KEY: str

    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUETS: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_FROM_NAME: str


settings: Setting = Setting()
