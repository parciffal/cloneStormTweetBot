from aiogram.filters.callback_data import CallbackData
from enum import StrEnum


class MediaActions(StrEnum):
    SHOW = "show"
    CHANGE = "change"
    ADD = "add"
    REMOVE = "remove"


class ShowMediaCallback(CallbackData, prefix="media"):
    group_id: int
    action: MediaActions
