from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import logging

from app.config import Config

router = Router()


@router.message(Command(commands=['close']), StateFilter("*"))
async def close_cmd_handler(message: Message, config: Config, state: FSMContext):
    try:
        await state.clear()
    except Exception as e:
        logging.error(e)


@router.message(Command(commands=['cancel']), StateFilter("*"))
async def cancel_cmd_handler(message: Message, config: Config, state: FSMContext):
    try:
        await message.delete()
        await state.clear()
    except Exception as e:
        logging.error(e)