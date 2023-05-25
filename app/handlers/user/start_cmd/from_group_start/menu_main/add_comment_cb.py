from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.db.models import GroupModel
from app.utils.callback_data.main_menu_cb_data import MenuActions, MainMenuCbData
from app.utils.callback_data.chg_comnt_cb_data import CommentActions, ChgCommentCbData
from app.keyboards.inline_keyboards.main_menu_kb import change_comment_kb, edit_comment_kb, remove_comment_kb
from app.utils.states.chg_comnt_state import ChgCommentState
import logging

router = Router()


@router.message(StateFilter(ChgCommentState.change_comment))
async def comment_message_text(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        group = await GroupModel.get(telegram_id=data['group_id'])
        group.comments = message.text
        await group.save()
        await state.clear()
        await message.delete()

        await data['message'].edit_text(
            f"New comment set!\n"
            f"Comment: <b>{group.comments}</b>",
            parse_mode="html")
        await data['message'].edit_reply_markup(await edit_comment_kb(group.telegram_id))
    except Exception as e:
        logging.error(e)


@router.callback_query(ChgCommentCbData.filter(F.action == CommentActions.CHANGE_COMMENT))
async def change_comment_cb(query: CallbackQuery, callback_data: ChgCommentCbData, state: FSMContext):
    try:
        await query.message.edit_text("Okay, enter the comment or enter /cancel to abort")
        await state.set_state(ChgCommentState.change_comment)
        await state.set_data({"group_id": callback_data.group_id,
                              "message": query.message})
    except Exception as e:
        logging.error(e)


@router.callback_query(ChgCommentCbData.filter(F.action == CommentActions.REMOVE_COMMENT))
async def remove_comment_cb(query: CallbackQuery, callback_data: ChgCommentCbData):
    try:
        await query.message.edit_text("Comment removed")
        await query.message.edit_reply_markup(await remove_comment_kb(callback_data.group_id))
    except Exception as e:
        logging.error(e)


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.ADD_COMMENT))
async def add_comment_cb(query: CallbackQuery, callback_data: MainMenuCbData):
    try:
        group_data = await GroupModel.get(telegram_id=callback_data.group_id)
        if query.message is not None:
            await query.message.edit_text(
                f"Comment: <b>{group_data.comments}</b>\n"
                f"Select an option below to change or remove comment",
                parse_mode="html")
            await query.message.edit_reply_markup(await change_comment_kb(callback_data.group_id))
    except Exception as e:
        logging.error(e)
