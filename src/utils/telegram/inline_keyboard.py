from pydantic import BaseModel
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.error import BadRequest

from src.utils.telegram.callback_data import format_callback_data_for_question


class KeyboardButtonForFormatting(BaseModel):
    text: str
    callback_data: str | None = None
    web_app_url: str | None = None


def format_inline_keyboard_for_question(choices: dict, question_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    choice,
                    callback_data=format_callback_data_for_question(choice=choice, question_id=question_id)
                ) for choice in choices.keys()
            ]
        ]
    )


def format_inline_keyboard(keyboard_buttons: list[KeyboardButtonForFormatting]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                keyboard_button.text,
                callback_data=keyboard_button.callback_data,
                web_app=WebAppInfo(url=keyboard_button.web_app_url) if keyboard_button.web_app_url else None
            )]
            for keyboard_button in keyboard_buttons
        ]
    )


async def remove_inline_keyboard(query: CallbackQuery) -> None:
    try:
        await query.edit_message_reply_markup()
    except BadRequest:
        pass
