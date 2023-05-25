from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from app.config import Config
from app.filters.is_owner import IsOwnerFilter


import logging

router = Router()


@router.message(Command(commands=['start']), IsOwnerFilter())
async def admin_menu_cmd(message: Message, config: Config):
    try:
        pass
    except Exception as e:
        logging.error(msg="admin_menu_cmd")
        logging.error(e)
