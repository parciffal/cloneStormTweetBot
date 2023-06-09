from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from app.db.models import GroupModel
from app.keyboards.inline_keyboards.main_menu_kb import return_kb
from app.utils.callback_data import MainMenuCbData, MenuActions

import logging

router = Router()


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.CH_INF_TWEETS))
async def ch_inf_tweets_cb(query: CallbackQuery, callback_data: MainMenuCbData):
    try:
        if await GroupModel.exists(telegram_id=callback_data.group_id):
            user = await GroupModel.get(telegram_id=callback_data.group_id)
            user.influencers_tweets = not user.influencers_tweets
            await user.save()
            markup = await return_kb(callback_data.group_id)
            if query.message:
                if user.influencers_tweets:
                    await query.message.edit_text(
                        "🎉Awesome, you're all set to receive alerts from now on.\n"
                        "Please Choose an option below"
                    )
                else:
                    await query.message.edit_text(
                        "Time to take a break from Tweet Alerts.\n"
                        "Please Choose an option below")
                await query.message.edit_reply_markup(markup)
    except Exception as e:
        logging.error(e)
