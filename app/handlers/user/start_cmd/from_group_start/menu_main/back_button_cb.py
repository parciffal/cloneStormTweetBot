from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.utils.callback_data.main_menu_cb_data import MenuActions, MainMenuCbData
from app.keyboards.inline_keyboards.main_menu_kb import main_menu_kb
from app.utils.tools import get_user_data, states_def

import logging

router = Router()


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.BACK_TO_MENU))
async def back_button_cb(query: CallbackQuery, callback_data: MainMenuCbData):
    try:
        if query.message is not None:
            group_data = await get_user_data(callback_data.group_id)

            keyboard = await main_menu_kb(group_data)
            await query.message.edit_text(
                f"⚒️ Group Settings\n"
                f"Raid Message: <b>{states_def[group_data['raid_msg']]}</b>\n"
                f"Include retweets and replies: <b>{states_def[group_data['retweets/replies']]}</b>\n"
                f"Comment in raid message: <b>{states_def[group_data['comment_raid_msg']]}</b>\n"
                f"Templates: <b>{group_data['templates_count']}/20</b> \n"
                f"Delay: <b>{group_data['delay']} Minutes </b>\n"
                f"Custom Twitter Account:\n <b>{group_data['account_count']}</b> Account Added\n"
                f"Select an option below to change settings",
                parse_mode="html")
            await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(e)