from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def group_init_keyboard(username, group_id, **kwargs) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Click me for settings", url=f"https://telegram.me/{username}?start={group_id}"),
        ]
    ])
