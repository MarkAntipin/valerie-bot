from pydantic import BaseModel


class TelegramUser(BaseModel):
    id: int  # noqa A003
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class User(BaseModel):
    user_id: int
    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
