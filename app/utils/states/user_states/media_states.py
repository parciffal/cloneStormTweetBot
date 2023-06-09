from aiogram.fsm.state import StatesGroup, State


class MediaState(StatesGroup):
    change_media = State()
    remove_media = State()
