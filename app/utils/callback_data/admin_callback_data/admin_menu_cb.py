from aiogram.filters.callback_data import CallbackData
from enum import StrEnum, IntEnum
from app.db.models import LeftTime


class AdminMenuActions(StrEnum):
    SHOW_ADS = "show"
    CONTINUE = "CONTINUE"
    DELETE_ADS = "delete"
    ADD_ADS = "add"
    EDIT_ADMIN_NAME = "edit_admin_name"
    SHOW_ADMIN_ADS = "show_admin_ads"
    BACK = "back"
    FINISH = "finish"


class AdminMenuCB(CallbackData, prefix="admin_menu"):
    user_id: int
    action: AdminMenuActions


class TimeDelay(IntEnum):
    DAY = 1
    WEEK = 7
    MONTH = 30
    YEAR = 365


class AdsDelayCB(CallbackData, prefix="ads_delay"):
    user_id: int
    delay: TimeDelay
