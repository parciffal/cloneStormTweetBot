from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import logging

from app.config import Config
from app.keyboards import group_init_keyboard
from app.filters.start_cmd_filters import GroupFilter
from app.db.models import UserModel, GroupModel

router = Router()


@router.message(Command(commands=['start']), GroupFilter())
async def start_handler(message: Message, config: Config):
    try:
        
        keyboard = group_init_keyboard(username=config.bot.username, group_id=message.chat.id, )
        await message.answer("Raiding Tweets made easy 🚀\n\n"
                             "I'll be leading raids for free and make it easier for the community.\n"
                             "Bot will send recent tweets by top influencers which the community "
                             "can raid.\n\n"
                             "To further simplify the process, you can set shill messages below "
                             "as templates to rally your community. 💬\n"
                             "It can also send tweets from your Project's official account only.\n\n"
                             "You can contact me if you're influencer who wants to get added.\n"
                             "For Support/Advertising: @cryptomoongives\n",
                             reply_markup=keyboard)
    except Exception as e:
        logging.error(e)

