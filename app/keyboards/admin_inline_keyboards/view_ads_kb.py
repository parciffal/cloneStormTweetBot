import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.models import AdminModel, AdsModel
from app.utils.callback_data.admin_callback_data.view_ads_cb import ViewAdsCB, ViewAdsActions
from app.utils.callback_data.admin_callback_data import AdsCB, AdsActions


async def ads_edit_kb(ads_id: int, admin: AdminModel) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Name",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.CHG_NAME
                                 ).pack()),
            InlineKeyboardButton(text="✏️ Description",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.CHG_DESC
                                 ).pack())
        ],
        [
            InlineKeyboardButton(text="📅 Delay",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.CHG_DELAY
                                 ).pack()),
            InlineKeyboardButton(text="🖼 Media",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.CHG_MEDIA
                                 ).pack())
        ],
        [
            InlineKeyboardButton(text="✏️ Show in Comment",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.CHG_SHOW_IN_COM
                                 ).pack()),
            InlineKeyboardButton(text="✏️ Show",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.CHG_SHOW
                                 ).pack())
        ],
        [
            InlineKeyboardButton(text="◀️ Back",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.BACK_TO_ADD
                                 ).pack()),
            InlineKeyboardButton(text="🗑 Del",
                                 callback_data=AdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=AdsActions.DELETE_ADS).pack())
        ]
    ])


async def ads_back_kb(ads_id: int, admin: AdminModel) -> InlineKeyboardMarkup:
    next_prew_buttons = []
    current_ads = await AdsModel.get(id=ads_id, admin=admin)
    ads = await AdsModel.filter(admin=admin)
    index = ads.index(current_ads)

    print(index)
    if index != 0:
        next_prew_buttons.append(InlineKeyboardButton(
            text="◀️ Pre",
            callback_data=AdsCB(
                user_id=admin.telegram_id,
                ads_id=ads[index-1].id,
                action=AdsActions.SHOW_ADS
            ).pack()))
    else:
        next_prew_buttons.append(InlineKeyboardButton(
            text="◀️ Pre",
            callback_data=AdsCB(
                user_id=admin.telegram_id,
                ads_id=ads[-1].id,
                action=AdsActions.SHOW_ADS
            ).pack()))
    if index != len(ads)-1:
        next_prew_buttons.append(InlineKeyboardButton(
            text="Next ▶️",
            callback_data=AdsCB(
                user_id=admin.telegram_id,
                ads_id=ads[index+1].id,
                action=AdsActions.SHOW_ADS
            ).pack()))
    else:
        next_prew_buttons.append(InlineKeyboardButton(
            text="Next ▶️",
            callback_data=AdsCB(
                user_id=admin.telegram_id,
                ads_id=ads[0].id,
                action=AdsActions.SHOW_ADS
            ).pack()))
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Edit",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.EDIT
                                 ).pack()),
            InlineKeyboardButton(text="🗑 Del",
                                 callback_data=AdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=AdsActions.DELETE_ADS).pack())
        ],
        next_prew_buttons,
        [
            InlineKeyboardButton(text="◀️ Back",
                                 callback_data=ViewAdsCB(
                                     user_id=admin.telegram_id,
                                     ads_id=ads_id,
                                     action=ViewAdsActions.BACK
                                 ).pack()),
        ]
    ])
