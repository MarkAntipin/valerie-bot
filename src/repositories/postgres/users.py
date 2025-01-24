import asyncpg


class UsersRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_by_telegram_id(self, telegram_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    user_id,
                    telegram_id,
                    first_name,
                    last_name,
                    username,
                    language_code,
                FROM
                    users
                WHERE
                    telegram_id = $1
                """,
                telegram_id
            )
        return row

    async def get_or_create(
        self,
        telegram_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        language_code: str | None = None,
    ) -> asyncpg.Record:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                    INSERT INTO users (
                        telegram_id,
                        first_name,
                        last_name,
                        username,
                        language_code
                    )
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (telegram_id)
                    DO UPDATE SET
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        username = EXCLUDED.username,
                        language_code = EXCLUDED.language_code
                    RETURNING
                        user_id,
                        telegram_id,
                        first_name,
                        last_name,
                        username,
                        language_code
                """,
                telegram_id,
                first_name,
                last_name,
                username,
                language_code,
            )
        return row
