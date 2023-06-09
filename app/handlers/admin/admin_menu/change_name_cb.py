from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, ContentType, FSInputFile
from aiogram.utils.text_decorations import html_decoration
from aiogram.fsm.context import FSMContext

from app.db.models import AdminModel
from app.keyboards.admin_inline_keyboards import get_admin_menu_kb, cancel_admin_kb, continue_admin_kb, \
    ads_delay_admin_kb
from app.utils.callback_data import AdminMenuCB, AdminMenuActions, AdsDelayCB
from app.utils.states.admin_states import ChangeNameState
from .admin_main_menu import admin_menu_cmd
import logging
router = Router()


@router.message(StateFilter(ChangeNameState.new_name), F.content_type.in_({ContentType.TEXT}))
async def edit_admin_chg_name(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        admin = data['admin']
        admin.name = message.text
        await admin.save()
        await state.clear()
        await message.delete()
        await admin_menu_cmd(message)
    except Exception as e:
        logging.error(e)


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.EDIT_ADMIN_NAME))
async def edit_admin_name_cb(query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.user_id)
        await state.set_data({"admin": admin})
        await query.message.edit_text(f"Your current name: {html_decoration.bold(admin.name)}\n"
                                      f"Send new name")
        await query.message.edit_reply_markup(await cancel_admin_kb(admin))
        await state.set_state(ChangeNameState.new_name)
    except Exception as e:
        logging.error(e)