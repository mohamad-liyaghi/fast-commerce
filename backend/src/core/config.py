from pydantic import BaseConfig
from decouple import Config, RepositoryEnv

env = Config(RepositoryEnv('env/.env'))


class Settings(BaseConfig):
    DEBUG: int = 0
    env: env = env
    POSTGRES_URL: str = (
        'postgresql+asyncpg://'
        f'{env.get("POSTGRES_USER")}:{env.get("POSTGRES_PASSWORD")}'
        f'@{env.get("POSTGRES_HOST")}/'
        f'{env.get("POSTGRES_DB")}'
    )
    TEST_POSTGRES_URL: str = (
        'postgresql+asyncpg://'
        f"{env.get('TEST_DB_USER')}:{env.get('TEST_DB_PASSWORD')}@"
        f"{env.get('TEST_DB_HOST')}/"
        f"{env.get('TEST_DB_NAME')}"
    )
    REDIS_URL: str = env.get('REDIS_URL')
    TEST_REDIS_URL: str = env.get('TEST_REDIS_URL')
    SECRET_KEY: str = env.get('SECRET_KEY')
    JWT_ALGORITHM: str = env.get('JWT_ALGORITHM')

    # Cache Keys:
    CACHE_USER_KEY: str = env.get('CACHE_USER_KEY')


settings: Settings = Settings()
