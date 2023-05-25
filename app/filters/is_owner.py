from aiogram.filters import Filter
from aiogram.types import Message
from app.config import Config


class IsOwnerFilter(Filter):

    async def __call__(self, message: Message, config: Config, *args, **kwargs) -> bool:
        return message.chat.type == "private" and message.chat.id in config.owners.owner_ids
