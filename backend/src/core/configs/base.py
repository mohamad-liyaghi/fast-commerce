from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """
    Base configuration class which loads environment variables from .env files.
    """

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


class PostgresConfig(BaseConfig):
    POSTGRES_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str


class TestPostgresConfig(BaseConfig):
    TEST_POSTGRES_URL: str
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str


class RedisConfig(BaseConfig):
    REDIS_URL: str
    TEST_REDIS_URL: str


class CeleryConfig(BaseConfig):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


class CacheConfig(BaseConfig):
    CACHE_USER_KEY: str
    CACHE_USER_TTL: int
    CACHE_CART_KEY: str


class JwtConfig(BaseConfig):
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUETS: int


class MailConfig(BaseConfig):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_FROM_NAME: str


class Settings(
    PostgresConfig,
    TestPostgresConfig,
    RedisConfig,
    CeleryConfig,
    CacheConfig,
    JwtConfig,
    MailConfig,
):
    pass


settings: Settings = Settings()
