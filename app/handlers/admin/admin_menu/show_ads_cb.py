from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, ContentType, FSInputFile
from aiogram.utils.text_decorations import html_decoration
from aiogram.fsm.context import FSMContext

from app.db.models import AdminModel
from app.keyboards.admin_inline_keyboards import cancel_admin_kb
from app.keyboards.admin_inline_keyboards.add_admin_ads_kb import ads_pagination
from app.utils.callback_data import AdminMenuCB, AdminMenuActions
from app.utils.callback_data.admin_callback_data import AdsCB, AdsActions, PaginationActions, PaginationCB
from app.utils.states.admin_states import ChangeNameState
from .admin_main_menu import admin_menu_cmd
import logging
router = Router()


@router.callback_query(PaginationCB.filter(F.action == PaginationActions.JUMP))
async def pagination_cb(query: CallbackQuery, callback_data: PaginationCB, state: FSMContext):
    try:
        data = await state.get_data()
        data['page'] = callback_data.page
        await state.set_data(data)
        page = await ads_pagination(data['admin'], data['page'])
        await state.set_data(data)
        await query.message.edit_reply_markup(page)
    except Exception as e:
        logging.error(e)


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.SHOW_ADS))
async def admin_ads_cb(query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.user_id)
        try:
            data = await state.get_data()
            data['admin'] = admin
            await state.set_data(data)
            page = await ads_pagination(admin, data['page'])
        except:
            await state.set_data({"admin": admin})
            page = await ads_pagination(admin)
        await query.message.edit_reply_markup(page)
    except Exception as e:
        logging.error(e)
