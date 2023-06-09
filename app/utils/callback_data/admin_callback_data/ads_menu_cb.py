from aiogram.filters.callback_data import CallbackData
from enum import StrEnum


class AdsActions(StrEnum):
    SHOW_ADS = "show_add"
    DELETE_ADS = "delete_add"


class AdsCB(CallbackData, prefix="ads"):
    user_id: int
    ads_id: int
    action: AdsActions


class PaginationActions(StrEnum):
    JUMP = "jump"
    HERE = "here"


class PaginationCB(CallbackData, prefix="pagination"):
    action: PaginationActions
    user_id: int
    page: int
