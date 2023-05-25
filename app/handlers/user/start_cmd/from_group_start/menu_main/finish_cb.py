from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboards.inline_keyboards.main_menu_kb import MenuActions, MainMenuCbData

import logging

router = Router()


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.FINISH), StateFilter("*"))
async def retweets_replies_cb(query: CallbackQuery, state: FSMContext):
    try:
        if query.message:
            await state.clear()
            await query.message.delete()
    except Exception as e:
        logging.error(e)
