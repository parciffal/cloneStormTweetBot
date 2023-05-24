from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from app.db.models import GroupModel
from app.keyboards.inline_keyboards.main_menu_kb.main_menu_kb import \
    (return_kb, MenuActions, MainMenuCbData)

import logging

router = Router()


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.RETWEETS_REPLIES))
async def retweets_replies_cb(query: CallbackQuery, callback_data: MainMenuCbData):
    try:
        user = await GroupModel.get(telegram_id=callback_data.group_id)
        user.retweets_replies = not user.retweets_replies
        await user.save()
        markup = await return_kb(callback_data.group_id)
        if user.retweets_replies:
            await query.message.edit_text(
                "🎉Awesome, you're all set to receive "
                "retweets and replies alerts from now on.\n"
                "Please Choose an option below")
        else:
            await query.message.edit_text(
                "Alright, you won't receive retweets"
                "and replies alerts from now on.\n"
                "Please Choose an option below")
        await query.message.edit_reply_markup(markup)
    except Exception as e:
        logging.error(e)
