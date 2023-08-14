from pydantic import BaseConfig


class Setting(BaseConfig):
    DEBUG: int = 0


setting: Setting = Setting()
