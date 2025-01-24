import json

import asyncpg

from src.models.places import TelegramIds


class MessagesRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def create_message(self, telegram_ids: list[TelegramIds], message_text: str, campaign_id: int) -> None:
        async with self.pg_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO messages (telegram_ids, message_text, campaign_id)
                VALUES ($1, $2, $3)
                """,
                json.dumps([t_ids.dict() for t_ids in telegram_ids]), message_text, campaign_id
            )

    async def get_by_campaign_id(self, campaign_id: int) -> list[asyncpg.Record]:
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    telegram_ids,
                    message_text,
                    campaign_id,
                    message_id
                FROM
                    messages
                WHERE
                    campaign_id = $1
                """,
                campaign_id
            )
        return rows

    async def get_by_id(self, message_id: int) -> asyncpg.Record:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    telegram_ids,
                    message_text,
                    campaign_id,
                    message_id
                FROM
                    messages
                WHERE
                    message_id = $1
                """,
                message_id
            )
        return row

    async def delete_message(self, message_id: int) -> None:
        async with self.pg_pool.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM messages
                WHERE message_id = $1
                """,
                message_id
            )
