import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.services.places import PlacesService
from src.texts import PLACES_NOT_FOUND_TEXT
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.send_message import send_message

logger = logging.getLogger(__name__)


async def find_place_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO: limit input message length
    logger.info('user %s run find_place_handler', update.message.from_user.id)

    places_service = PlacesService(pg_pool=pg_pool)

    query: str = update.message.text

    res: str | None = await places_service.find_places(query=query)

    await send_message(
        message=update.message,
        text=res if res else PLACES_NOT_FOUND_TEXT,
    )
