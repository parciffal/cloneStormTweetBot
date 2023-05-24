from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import Config

router = Router()


@router.message(Command(commands=['enable']))
async def enable_handler(message: Message, config: Config):
    await message.answer("Start receiving alerts")
