from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from app.utils.callback_data.main_menu_cb_data import MenuActions, MainMenuCbData
from app.utils.callback_data.change_delay_cb_data import DelayEnum, ChgDelayCbData


async def change_delay_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="5 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.FIVE,
                                     group_id=group_id
                                 ).pack()),
            InlineKeyboardButton(text="10 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.TEN,
                                     group_id=group_id
                                 ).pack()),
            InlineKeyboardButton(text="15 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.FIFTEEN,
                                     group_id=group_id
                                 ).pack()),
        ],
        [
            InlineKeyboardButton(text="20 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.TWENTY,
                                     group_id=group_id
                                 ).pack()),
            InlineKeyboardButton(text="25 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.TWENTY_FIVE,
                                     group_id=group_id
                                 ).pack()),
            InlineKeyboardButton(text="30 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.THIRTY,
                                     group_id=group_id
                                 ).pack()),
        ],
        [
            InlineKeyboardButton(text="35 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.THIRTY_FIVE,
                                     group_id=group_id
                                 ).pack()),
            InlineKeyboardButton(text="40 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.FORTY,
                                     group_id=group_id
                                 ).pack()),
            InlineKeyboardButton(text="45 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.FORTY_FIVE,
                                     group_id=group_id
                                 ).pack()),
        ],
        [
            InlineKeyboardButton(text="50 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.FIFTY,
                                     group_id=group_id
                                 ).pack()),
            InlineKeyboardButton(text="55 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.FIFTY_FIVE,
                                     group_id=group_id
                                 ).pack()),
            InlineKeyboardButton(text="60 Minutes",
                                 callback_data=ChgDelayCbData(
                                     action=DelayEnum.SIXTY,
                                     group_id=group_id
                                 ).pack()),
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
