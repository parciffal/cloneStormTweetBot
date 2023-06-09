from aiogram.filters.callback_data import CallbackData
from enum import StrEnum


class PrivateActions(StrEnum):
    GROUPS = "my_groups"


class PrivateStartCallback(CallbackData, prefix="private_start"):
    group_id: int
    user_id: int
    action: PrivateActions
