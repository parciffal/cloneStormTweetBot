from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class DelayEnum(IntEnum):
    FIVE = 5
    TEN = 10
    FIFTEEN = 15
    TWENTY = 20
    TWENTY_FIVE = 25
    THIRTY = 30
    THIRTY_FIVE = 35
    FORTY = 40
    FORTY_FIVE = 45
    FIFTY = 50
    FIFTY_FIVE = 55
    SIXTY = 60


class ChgDelayCbData(CallbackData, prefix="delay"):
    action: DelayEnum
    group_id: int
