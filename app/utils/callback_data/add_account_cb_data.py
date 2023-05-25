import enum

from aiogram.filters.callback_data import CallbackData


class AccountActions(str, enum.Enum):
    REMOVE_ACCOUNT = "remove_account"


class AddAccountCbData(CallbackData, prefix="account"):
    action: AccountActions
    group_id: int
    account_id: int
