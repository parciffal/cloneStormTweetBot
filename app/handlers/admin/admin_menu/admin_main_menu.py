import aiogram.types.message
from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, MessageEntity, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.message import html_decoration


from app.config import Config
from app.filters.is_owner import IsOwnerFilter
from app.db.models import AdminModel
from app.utils.callback_data import AdminMenuCB, AdminMenuActions
from app.utils.tools.admin_data_tools import states_def
from app.keyboards.admin_inline_keyboards.admin_menu_kb import get_admin_menu_kb
import logging

router = Router()


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.BACK), StateFilter('*'))
async def admin_back_cb(query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext):
    try:
        await state.clear()
        await query.message.delete()
        await admin_menu_cmd(query.message)
    except Exception as e:
        logging.error(e)


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.FINISH), StateFilter('*'))
async def admin_finish_cb(query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext):
    try:
        await state.clear()
        await query.message.delete()
    except Exception as e:
        logging.error(e)


@router.message(Command(commands=['admin']), IsOwnerFilter())
async def admin_menu_cmd(message: Message):
    try:
        if not await AdminModel.exists(telegram_id=message.chat.id):
            admin = await AdminModel.create(
                telegram_id=message.chat.id,
                name=message.chat.username if message.chat.username else str(message.chat.id))
            await admin.save()
        admin = await AdminModel.get(telegram_id=message.chat.id)
        keyboard = await get_admin_menu_kb(admin)

        await message.answer(
            text=f"<b>Admin Panel</b>\n\n"
                 f"Name: {html_decoration.bold(admin.name)}\n"
                 f"Telegram_id: {html_decoration.spoiler(admin.telegram_id)}\n"
                 f"Show ads: {html_decoration.bold(states_def[admin.show_adds])}\n"
                 f"\nChoose Ads to edit\n",
            parse_mode="html",
            reply_markup=keyboard)
    except Exception as e:
        logging.error(msg="admin_menu_cmd")
        logging.error(e)
