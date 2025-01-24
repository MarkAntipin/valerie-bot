
import asyncpg


def _embedding_to_str(embedding: list[float]) -> str:
    return "[" + ",".join(map(str, embedding)) + "]"


class PlacesRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def find_simular(self, embedding: list[float], limit: int = 3) -> list[asyncpg.Record]:
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch(
                'SELECT place_id, metadata, embedding <-> $1 as dist FROM places '
                ' ORDER BY embedding <-> $1 LIMIT $2',
                _embedding_to_str(embedding),
                limit,
            )
        return rows
