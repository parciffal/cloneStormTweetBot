from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.filters.start_cmd_filters import FromGroupFilter
from app.utils.callback_data.private_start_cb_data import PrivateStartCallback, PrivateActions
from app.keyboards.inline_keyboards.main_menu_kb import main_menu_kb
from app.utils.tools import get_user_data, states_def

import logging

router = Router()


@router.callback_query(PrivateStartCallback.filter(F.action == PrivateActions.GROUPS))
async def group_settings_cb(query: CallbackQuery, callback_data: PrivateStartCallback):
    try:
        group_id = callback_data.group_id
        group_data = await get_user_data(int(group_id))

        keyboard = await main_menu_kb(group_data)
        await query.message.edit_text(
                f"⚒️ Group Settings\n"
                f"Raid Message: <b>{states_def[group_data['raid_msg']]}</b>\n"
                f"Include retweets and replies: <b>{states_def[group_data['retweets/replies']]}</b>\n"
                f"Comment in raid message: <b>{states_def[group_data['comment_raid_msg']]}</b>\n"
                f"Templates: <b>{group_data['templates_count']}/20</b> \n"
                f"Delay: <b>{group_data['delay']} Minutes </b>\n"
                f"Custom Twitter Account:\n <b>{group_data['account_count']}</b> Account Added\n"
                f"Select an option below to change settings\n"
                f"To remove delete bot from Group",
                parse_mode="HTML",)
        await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(e)


@router.message(Command(commands=['start']), FromGroupFilter())
async def start_handler(message: Message):
    try:
        group_id = message.text.split(" ")[1]
        group_data = await get_user_data(int(group_id))

        keyboard = await main_menu_kb(group_data)
        await message.answer(
                f"⚒️ Group Settings\n"
                f"Raid Message: <b>{states_def[group_data['raid_msg']]}</b>\n"
                f"Include retweets and replies: <b>{states_def[group_data['retweets/replies']]}</b>\n"
                f"Comment in raid message: <b>{states_def[group_data['comment_raid_msg']]}</b>\n"
                f"Templates: <b>{group_data['templates_count']}/20</b> \n"
                f"Delay: <b>{group_data['delay']} Minutes </b>\n"
                f"Custom Twitter Account:\n <b>{group_data['account_count']}</b> Account Added\n"
                f"Select an option below to change settings"
                f"To remove delete bot from Group",
                parse_mode="HTML",
                reply_markup=keyboard)
    except Exception as e:
        logging.error(e)
