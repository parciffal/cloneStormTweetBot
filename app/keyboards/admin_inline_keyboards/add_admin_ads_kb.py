from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.models import AdminModel, AdsModel
from app.utils.callback_data.admin_callback_data import (AdsCB, AdsActions, PaginationActions,
                                                         PaginationCB, AdminMenuCB, AdminMenuActions)

position_states = [
    "first",
    "middle",
    "last"
]


async def ads_pagination_old(admin: AdminModel, page: int = 2) -> InlineKeyboardMarkup:
    ads = await AdsModel.filter(admin=admin)
    pages = len(ads) / 5
    print(pages)
    ads_count = len(ads)
    print(ads_count)
    send_ads: list[AdsModel]
    if page == 1:
        if ads_count >= 5:
            send_ads = ads[:5]
        else:
            send_ads = ads
    elif page == pages - 1:
        if ads_count - page * 5 <= 5:
            send_ads = ads[(page - 1) * 5:]
        else:
            send_ads = ads[(page - 1) * 5: (page + 1) * 5]
    else:
        send_ads = ads[(page - 1) * 5: (page + 1) * 5]
    print(send_ads)
    kb = await generate_ads_keyboard(send_ads, admin, page, pages)
    return kb


async def ads_pagination(admin: AdminModel, page: int = 1, page_size: int = 5) -> InlineKeyboardMarkup:
    offset = (page - 1) * page_size
    query = AdsModel.filter(admin=admin).offset(offset).limit(page_size)
    ads = await query
    page_count = await AdsModel.filter(admin=admin)
    page_count = len(page_count)/page_size
    if page_count > int(page_count):
        page_count = int(page_count)+1
    else:
        page_count = int(page_count)

    keyboard = await generate_ads_keyboard(ads, admin, page, page_count)
    return keyboard


async def generate_ads_keyboard(ads: list[AdsModel], admin: AdminModel, position: int, pages: int) -> InlineKeyboardMarkup:
    ads_buttons = [
        [InlineKeyboardButton(
            text=i.name if i.name != "" else str(i.id),
            callback_data=AdsCB(
                action=AdsActions.SHOW_ADS,
                ads_id=i.id,
                user_id=admin.telegram_id).pack())] for i in ads
    ]
    page_buttons = []
    if 1 <= position <= round(pages):
        start = 1
        end = round(pages)
    else:
        start = position - 2
        end = position + 2
    for i in range(start, end + 1):
        if i == position:
            page_buttons.append(InlineKeyboardButton(
                text=f"-{i}-",
                callback_data=PaginationCB(
                    action=PaginationActions.HERE,
                    user_id=admin.telegram_id,
                    page=i
                ).pack()
            ))
        else:
            page_buttons.append(InlineKeyboardButton(
                text=f"{str(i)}",
                callback_data=PaginationCB(
                    action=PaginationActions.JUMP,
                    user_id=admin.telegram_id,
                    page=i
                ).pack()
            ))
    back_buttons = [
        InlineKeyboardButton(
            text="Back",
            callback_data=AdminMenuCB(
                action=AdminMenuActions.BACK,
                user_id=admin.telegram_id
            ).pack()
        ),
        InlineKeyboardButton(
            text="Finish",
            callback_data=AdminMenuCB(
                action=AdminMenuActions.FINISH,
                user_id=admin.telegram_id
            ).pack()
        )
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            *ads_buttons,
            page_buttons,
            back_buttons
        ]
    )
