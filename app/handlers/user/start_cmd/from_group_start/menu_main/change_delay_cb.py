from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.inline_keyboards.main_menu_kb import MenuActions, MainMenuCbData, return_kb
from app.keyboards.inline_keyboards.main_menu_kb import change_delay_kb, ChgDelayCbData
from app.db.models import GroupModel

import logging

router = Router()


@router.callback_query(ChgDelayCbData.filter())
async def set_new_delay_cb(query: CallbackQuery, callback_data: MainMenuCbData):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)
        group.delay = callback_data.action
        await group.save()
        await query.message.edit_text(
            "New delay set!")
        await query.message.edit_reply_markup(
            await return_kb(callback_data.group_id)
        )
    except Exception as e:
        logging.error(e)


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.CHANGE_DELAY))
async def change_delay_cb(query: CallbackQuery, callback_data: MainMenuCbData):
    try:
        await query.message.edit_text(
            "Click on delay below to set")
        await query.message.edit_reply_markup(
            await change_delay_kb(callback_data.group_id))
    except Exception as e:
        logging.error(e)
