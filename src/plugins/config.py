from pydantic import BaseSettings

class Config(BaseSettings):

    plugin_setting: str = 'default'

    class Config:
        extra = 'ignore'