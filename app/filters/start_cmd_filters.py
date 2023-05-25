from typing import Any, Union, Dict

from aiogram.filters import Filter
from aiogram.types import Message

from app.db.models import UserModel


class UserProfileFilter(Filter):
    async def __call__(self, message: Message, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        return await UserModel.exists(telegram_id=message.chat.id) and message.chat.type == "private"


class PrivateChatFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private" and message.text.find("-") == -1


class GroupFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type != "private"


class FromGroupFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private" and message.text.find("-") != -1
