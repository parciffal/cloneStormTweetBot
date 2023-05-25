from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def group_init_keyboard(username: str, group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Click me for settings", url=f"https://telegram.me/{username}?start={group_id}"),
        ]
    ])
