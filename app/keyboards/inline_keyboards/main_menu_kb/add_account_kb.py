from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.all_in_one_models import AccountModel
from app.utils.callback_data.main_menu_cb_data import MenuActions, MainMenuCbData
from app.utils.callback_data.add_account_cb_data import AccountActions, AddAccountCbData


async def add_account_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Add Account",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.ADD_ACCOUNT,
                                     group_id=group_id
                                 ).pack())
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
    ])


async def show_account_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Show Account",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.ADD_ACCOUNT,
                                     group_id=group_id
                                 ).pack())
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


async def remove_account_kb(accounts: List[AccountModel], group_id: int) -> InlineKeyboardMarkup:
    account_buttons = [
        InlineKeyboardButton(text=i.name,
                              callback_data=AddAccountCbData(
                                action=AccountActions.REMOVE_ACCOUNT,
                                group_id=group_id,
                                account_id=i.id
                              ).pack()) for i in accounts]
    return InlineKeyboardMarkup(inline_keyboard=[
        account_buttons,
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
    ])