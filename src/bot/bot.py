
from ptbcontrib.postgres_persistence import PostgresPersistence
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from settings import PostgresSettings, bot_settings
from src.bot.handlers.commands import (
    start_handler,
)
from src.bot.handlers.error import error_handler
from src.bot.handlers.find_place import find_place_handler
from src.bot.states import (
    BotStates,
)


def create_bot() -> Application:
    # logging.basicConfig(level=logging.INFO)

    pg_settings = PostgresSettings()
    persistence = PostgresPersistence(url=pg_settings.url_for_persistence)
    bot = Application.builder().token(bot_settings.TOKEN).persistence(persistence).build()

    # conversation handler
    bot.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler)
        ],
        states={
            BotStates.find_place: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, find_place_handler)
            ],
        },
        fallbacks=[]
    ))

    # error handler
    bot.add_error_handler(error_handler)

    # commands
    bot.add_handler(CommandHandler('start', start_handler))

    return bot
