from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.inline_keyboards.main_menu_kb.main_menu_kb import \
    ( MenuActions, MainMenuCbData)

import logging

router = Router()


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.FINISH))
async def retweets_replies_cb(query: CallbackQuery, callback_data: MainMenuCbData):
    try:
        if query.message:
            await query.message.delete()
    except Exception as e:
        logging.error(e)
