from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.callback_data.main_menu_cb_data import MainMenuCbData, MenuActions
from app.utils.callback_data.private_start_cb_data import PrivateStartCallback, PrivateActions
from app.db.models import GroupModel


async def user_profile_kb(groups: List[GroupModel], user_id: int) -> InlineKeyboardMarkup:
    groups_buttons = [
        InlineKeyboardButton(text=i.name if i.name != "" else i.telegram_id,
                             callback_data=PrivateStartCallback(
                                 action=PrivateActions.GROUPS,
                                 group_id=i.telegram_id,
                                 user_id=user_id
                             ).pack()) for i in groups]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            groups_buttons,
            [
                InlineKeyboardButton(text="Finish",
                                     callback_data=MainMenuCbData(
                                         action=MenuActions.FINISH,
                                         group_id=user_id).pack())
            ]
        ]
    )
