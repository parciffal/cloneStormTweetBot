from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.inline_keyboards.main_menu_kb.main_menu_kb import \
    ( MenuActions, MainMenuCbData)
from app.db.models import GroupModel

import logging

router = Router()


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.CHANGE_DELAY))
async def change_delay_cb(query: CallbackQuery, callback_data: MainMenuCbData):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)

    except Exception as e:
        logging.error(e)