import asyncpg

from src.mappers.users import map_user_from_pg_row
from src.models.users import TelegramUser, User
from src.repositories.postgres.users import UsersRepo


class UsersService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.users_repo = UsersRepo(pg_pool=pg_pool)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        row = await self.users_repo.get_by_telegram_id(telegram_id=telegram_id)
        return map_user_from_pg_row(row=row) if row else None

    async def get_or_create(self, tg_user: TelegramUser) -> User:
        row = await self.users_repo.get_or_create(
            telegram_id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username,
            language_code=tg_user.language_code,
        )
        return map_user_from_pg_row(row=row)
