from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.utils.text_decorations import html_decoration

from app.db.models import AdminModel, AdsModel
from app.keyboards.admin_inline_keyboards import get_admin_menu_kb
from app.utils.callback_data import AdminMenuCB, AdminMenuActions
from app.utils.tools.admin_data_tools import states_def
from .admin_main_menu import admin_menu_cmd
import logging

router = Router()


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.SHOW_ADMIN_ADS))
async def show_admin_ads_cb(query: CallbackQuery, callback_data: AdminMenuCB):
    try:
        if await AdminModel.exists(telegram_id=callback_data.user_id):
            admin = await AdminModel.get(telegram_id=callback_data.user_id)
            admin.show_adds = not admin.show_adds
            await admin.save()
            await admin_menu_cmd(query.message)
    except Exception as e:
        logging.error(e)
