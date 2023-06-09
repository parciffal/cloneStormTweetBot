from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.callback_data import MainMenuCbData, MenuActions
from app.utils.callback_data import ShowMediaCallback, MediaActions


async def no_media_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Add Media",
                                     callback_data=ShowMediaCallback(
                                         action=MediaActions.ADD,
                                         group_id=group_id).pack())
            ],
            [
                InlineKeyboardButton(text="Back to Menu",
                                     callback_data=MainMenuCbData(
                                         action=MenuActions.BACK_TO_MENU,
                                         group_id=group_id).pack()),
                InlineKeyboardButton(text="Finish",
                                     callback_data=MainMenuCbData(
                                         action=MenuActions.FINISH,
                                         group_id=group_id).pack())

            ]
        ]
    )


async def show_media_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Change Media",
                                 callback_data=ShowMediaCallback(
                                    action=MediaActions.CHANGE,
                                    group_id=group_id).pack())
        ],
        [
            InlineKeyboardButton(text="Remove",
                                 callback_data=ShowMediaCallback(
                                     action=MediaActions.REMOVE,
                                     group_id=group_id).pack())
        ],
        [
            InlineKeyboardButton(text="Back to Menu",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.BACK_TO_MENU,
                                     group_id=group_id).pack()),
        ],

    ]
    )
