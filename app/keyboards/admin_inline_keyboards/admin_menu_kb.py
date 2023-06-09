from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.callback_data import MainMenuCbData, MenuActions, AdsDelayCB,\
                                    AdminMenuActions, AdminMenuCB, TimeDelay
from app.db.models import AdsModel, AdminModel


async def get_admin_menu_kb(admin: AdminModel) -> InlineKeyboardMarkup:
    show_ads = "✅ Show Ads"
    if not admin.show_adds:
        show_ads = "❌ Show Ads"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Ads",
                                     callback_data=AdminMenuCB(
                                         action=AdminMenuActions.ADD_ADS,
                                         user_id=admin.telegram_id
                                     ).pack()),

                InlineKeyboardButton(text="✏️ Name",
                                     callback_data=AdminMenuCB(
                                        action=AdminMenuActions.EDIT_ADMIN_NAME,
                                        user_id=admin.telegram_id
                                     ).pack()),
            ],
            [
                InlineKeyboardButton(text=show_ads,
                                     callback_data=AdminMenuCB(
                                         action=AdminMenuActions.SHOW_ADMIN_ADS,
                                         user_id=admin.telegram_id
                                     ).pack()),

                InlineKeyboardButton(text="🗂 Ads",
                                     callback_data=AdminMenuCB(
                                         action=AdminMenuActions.SHOW_ADS,
                                         user_id=admin.telegram_id
                                     ).pack())
            ],
            [
                InlineKeyboardButton(text="🏁 Finish",
                                     callback_data=MainMenuCbData(
                                         action=MenuActions.FINISH,
                                         group_id=admin.telegram_id).pack())
            ]
        ]
    )


async def cancel_admin_kb(admin: AdminModel) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Back",
                                 callback_data=AdminMenuCB(
                                     action=AdminMenuActions.BACK,
                                     user_id=admin.telegram_id
                                 ).pack()),
            InlineKeyboardButton(text="🏁 Finish",
                                 callback_data=AdminMenuCB(
                                     action=AdminMenuActions.BACK,
                                     user_id=admin.telegram_id
                                 ).pack())
        ],
    ])


async def continue_admin_kb(admin: AdminModel) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Continue",
                                 callback_data=AdminMenuCB(
                                     action=AdminMenuActions.CONTINUE,
                                     user_id=admin.telegram_id
                                 ).pack())
        ],
        [
            InlineKeyboardButton(text="◀️ Back",
                                 callback_data=AdminMenuCB(
                                     action=AdminMenuActions.BACK,
                                     user_id=admin.telegram_id
                                 ).pack()),
            InlineKeyboardButton(text="🏁 Finish",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.FINISH,
                                     group_id=admin.telegram_id).pack())
        ],
    ])


async def ads_delay_admin_kb(admin: AdminModel) -> InlineKeyboardMarkup:
    delay_buttons = [
        InlineKeyboardButton(
            text=i.name,
            callback_data=AdsDelayCB(
                delay=i.value,
                user_id=admin.telegram_id
            ).pack()
        )
        for i in TimeDelay]
    return InlineKeyboardMarkup(inline_keyboard=[
        delay_buttons,

        [
            InlineKeyboardButton(text="◀️ Back",
                                 callback_data=AdminMenuCB(
                                     action=AdminMenuActions.BACK,
                                     user_id=admin.telegram_id
                                 ).pack()),
            InlineKeyboardButton(text="🏁 Finish",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.FINISH,
                                     group_id=admin.telegram_id).pack())
        ],
    ])

