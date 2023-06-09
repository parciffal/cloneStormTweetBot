from aiogram.fsm.state import StatesGroup, State


class AddAdsState(StatesGroup):
    add_ads = State()
    ads_name = State()
    ads_description = State()
    ads_media = State()
    ads_left_time = State()


class EditAdsState(StatesGroup):
    add_ads = State()
    ads_name = State()
    ads_description = State()
    ads_media = State()
    ads_left_time = State()
