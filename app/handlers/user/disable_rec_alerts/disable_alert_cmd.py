from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import Config

router = Router()


@router.message(Command(commands=['disable']))
async def disable_handler(message: Message, config: Config):
    await message.answer("Stop receiving alerts")
