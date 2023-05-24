from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER

import logging

from app.config import Config
from app.keyboards import first_start_keyboard
from app.filters.start_cmd_filters import PrivateChatFilter
from app.utils.callback_data.private_start_cb_data import PrivateStartCallback
from app.db.models import UserModel, GroupModel

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> IS_NOT_MEMBER))
async def bot_removed_as_member(event: ChatMemberUpdated, bot: Bot):
    try:
        print("Group deleted from db")
        if await GroupModel.exists(telegram_id=event.chat.id):
            group = await GroupModel.get(telegram_id=event.chat.id)
            await group.delete()
    except Exception as e:
        logging.error(e)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    try:
        chat_info = await bot.get_chat(event.chat.id)
        print(event.chat)
        if bool(chat_info.permissions.can_send_messages):
            if not await GroupModel.exists(telegram_id=event.chat.id):
                if await UserModel.exists(telegram_id=event.from_user.id):
                    print(f"Group {event.chat.title} added to db")
                    user = await UserModel.get(telegram_id=event.from_user.id)
                    group = await GroupModel.create(telegram_id=event.chat.id,
                                                    name=event.chat.title,
                                                    user=user)
                    await group.save()
                else:
                    await bot.send_message(event.from_user.id, f"Bot is already in group")
    except Exception as e:
        logging.error(e)


@router.message(Command(commands=['start']), PrivateChatFilter())
async def start_handler(message: Message, config: Config):
    try:
        if not await UserModel.exists(telegram_id=message.chat.id):
            user = await UserModel.create(telegram_id=message.chat.id)
            await user.save()
        keyboard = first_start_keyboard(config.bot.username)
        await message.answer("Raiding Tweets made easy 🚀\n\n"
                             "I'll be leading raids for free and make it"
                             " easier for the community.\n"
                             "Bot will send recent tweets by top influencers which the community can raid.\n"
                             "To further simplify the process, you can set shill messages below as templates to "
                             "rally"
                             "your community. 💬\n"
                             "It can also send tweets from your Project's official account only.\n"
                             "You can contact me if you're influencer who wants to get added.\n\n"
                             "For Support/Advertising: @cryptomoongives",
                             reply_markup=keyboard)
    except Exception as e:
        logging.error(e)
