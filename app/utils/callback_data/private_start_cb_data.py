from aiogram.filters.callback_data import CallbackData


class PrivateStartCallback(CallbackData, prefix="private_start"):
    user_id: int
    action: str



