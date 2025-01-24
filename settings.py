from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(BASE_DIR, 'images')

ENV_FILE = Path(BASE_DIR, '.env')
load_dotenv(ENV_FILE)


class PostgresSettings(BaseSettings):
    HOST: str = 'localhost'
    USER: str = 'valerie'
    PASSWORD: str = 'valerie'
    DATABASE: str = 'valerie'
    PORT: int = 5432

    @property
    def url(self) -> str:
        return f'postgres://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    @property
    def url_for_persistence(self) -> str:
        return f'postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    class Config:
        case_sensitive = False
        env_prefix = "PG_"


class BotSettings(BaseSettings):
    TOKEN: str
    OPENAI_KEY: str

    IS_DEBUG: bool = False

    class Config:
        case_sensitive = False


bot_settings = BotSettings()
