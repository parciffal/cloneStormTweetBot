from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.db.models import GroupModel, AccountModel
from app.utils.callback_data import MenuActions, MainMenuCbData
from app.utils.callback_data import AccountActions, AddAccountCbData

from app.utils.states.user_states import AddAccountState

from app.keyboards.inline_keyboards.main_menu_kb import show_account_kb, remove_account_kb, add_account_kb

import logging

router = Router()


@router.message(StateFilter(AddAccountState.add_account))
async def account_message_text(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        group = await GroupModel.get(telegram_id=data['group_id'])

        if message.text.startswith('@') and len(message.text) < 40:
            acc = await AccountModel.create(name=message.text, group=group)
            await acc.save()
            await state.clear()
            await message.delete()

            await data['message'].edit_text(
                f"Show Account!")
            await data['message'].edit_reply_markup(await show_account_kb(group.telegram_id))
        else:
            await message.delete()
            await state.set_state(AddAccountState.add_account)
            await data['message'].edit_text(
                "Invalid username\n"
                "Please enter it again in @username format"
            )
    except Exception as e:
        logging.error(e)


@router.callback_query(AddAccountCbData.filter(F.action == AccountActions.REMOVE_ACCOUNT))
async def remove_account_cb(query: CallbackQuery, callback_data: AddAccountCbData):
    try:
        account = await AccountModel.get(id=callback_data.account_id)
        await account.delete()
        await query.message.edit_text("Click on account username to remove it or you can add account")
        await query.message.edit_reply_markup(await add_account_kb(callback_data.group_id))
    except Exception as e:
        logging.error(e)


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.ADD_ACCOUNT))
async def add_account_cb(query: CallbackQuery, callback_data: MainMenuCbData, state: FSMContext):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)
        accounts = await AccountModel.filter(group=group)
        if len(accounts) == 0:
            await state.set_state(AddAccountState.add_account)
            await state.set_data({"group_id": callback_data.group_id,
                                  "message": query.message})
            await query.message.edit_text(
                "Okey enter Twitter username in @username format or enter /cancel to abort")
        else:
            await query.message.edit_text("Click on account to remove it")
            await query.message.edit_reply_markup(await remove_account_kb(accounts, callback_data.group_id))
    except Exception as e:
        logging.error(e)
