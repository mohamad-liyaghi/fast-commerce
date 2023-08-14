from pydantic import BaseConfig
from decouple import Config, RepositoryEnv

env = Config(RepositoryEnv('env/.env'))


class Settings(BaseConfig):
    DEBUG: int = 0
    env: str = env
    POSTGRES_URL: str = (
        'postgresql://'
        f'{env.get("POSTGRES_USER")}:{env.get("POSTGRES_PASSWORD")}'
        f'@{env.get("POSTGRES_HOST")}/'
        f'{env.get("POSTGRES_DB")}'
    )


settings: Settings = Settings()
