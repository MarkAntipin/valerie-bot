import json

import asyncpg

from src.models.places import Place, PlaceMetadata


def map_place_from_pg_row(row: asyncpg.Record) -> Place:
    return Place(
        place_id=row['place_id'],
        metadata=PlaceMetadata(**json.loads(row['metadata']))
    )

