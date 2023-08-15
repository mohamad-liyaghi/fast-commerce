from pydantic import BaseConfig
from decouple import Config, RepositoryEnv

env = Config(RepositoryEnv('env/.env'))


class Settings(BaseConfig):
    DEBUG: int = 0
    env: env = env
    POSTGRES_URL: str = (
        'postgresql://'
        f'{env.get("POSTGRES_USER")}:{env.get("POSTGRES_PASSWORD")}'
        f'@{env.get("POSTGRES_HOST")}/'
        f'{env.get("POSTGRES_DB")}'
    )
    REDIS_URL: str = env.get('REDIS_URL')


settings: Settings = Settings()
