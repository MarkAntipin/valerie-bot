import logging
import pathlib

from telegram import Bot, InlineKeyboardMarkup, Message, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.error import Forbidden

from src.utils.telegram.inline_keyboard import (
    KeyboardButtonForFormatting,
    format_inline_keyboard,
)

logger = logging.getLogger(__name__)


async def _send_message(
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None,
    photo_path: pathlib.Path = None
) -> bool:
    if not message and not bot:
        raise ValueError('message or bot should be passed to send message')

    if not reply_markup:
        reply_markup = ReplyKeyboardRemove()
    parse_mode = ParseMode.MARKDOWN_V2
    try:
        if message:
            if photo_path:
                await message.reply_photo(
                    photo=photo_path,
                    caption=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                )
            else:
                await message.reply_text(
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                )
        elif bot:
            if photo_path:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_path,
                    caption=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                )
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                )
    except Forbidden:
        logger.error('User has blocked bot')
        return False

    return True


async def send_message(
    text: str,
    keyboard_buttons: list[KeyboardButtonForFormatting] | None = None,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None,
) -> bool:
    return await _send_message(
        message=message,
        bot=bot,
        chat_id=chat_id,
        text=text,
        reply_markup=format_inline_keyboard(keyboard_buttons=keyboard_buttons) if keyboard_buttons else None,
    )
