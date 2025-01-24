import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import ContextTypes

from src.bot.states import BotStates
from src.mappers.users import map_inner_telegram_user_from_tg_user
from src.services.users import UsersService
from src.texts import START_TEXT
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.send_message import send_message

logger = logging.getLogger(__name__)


async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    tg_user: TGUser = update.message.from_user
    logger.info('user %s run start_handler', tg_user.id)

    users_service = UsersService(pg_pool=pg_pool)
    await users_service.get_or_create(tg_user=map_inner_telegram_user_from_tg_user(tg_user))

    await send_message(
        message=update.message,
        text=START_TEXT,
    )
    return BotStates.find_place


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass
