from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, ContentType, FSInputFile
from aiogram.utils.text_decorations import html_decoration
from aiogram.fsm.context import FSMContext

from app.db.models import AdminModel, AdsModel
from app.filters.is_owner import IsOwnerFilter
from app.keyboards.admin_inline_keyboards import get_admin_menu_kb, cancel_admin_kb, continue_admin_kb, \
    ads_delay_admin_kb
from app.utils.callback_data import AdminMenuCB, AdminMenuActions, AdsDelayCB
from app.utils.states.admin_states import AddAdsState

import logging
from datetime import datetime, timedelta

router = Router()


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.CONTINUE))
async def continue_ads_cb(query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext):
    try:
        data = await state.get_data()

        await state.set_state(AddAdsState.ads_left_time)
        await query.message.answer("Now choose timedelay in which ads would be shown",
                                   reply_markup=await ads_delay_admin_kb(data['admin']))
    except Exception as e:
        logging.error(e)


@router.callback_query(StateFilter(AddAdsState.ads_left_time), AdsDelayCB.filter())
async def add_delay_ads_cb(query: CallbackQuery, callback_data: AdsDelayCB, state: FSMContext):
    try:
        data = await state.get_data()
        delay = callback_data.delay
        data['delay'] = delay
        admin = data['admin']
        try:
            media = data['media']
        except:
            media = ""
        name = data['name']
        description = data['description']
        ads = await AdsModel.create(name=name,
                                    description=description,
                                    media=media,
                                    left_time=datetime.now()+timedelta(int(delay)),
                                    admin=admin)
        await ads.save()
        text = f"<b>Ads added</b>\n" \
               f"<b>Name</b>: {name}\n" \
               f"<b>Description</b>:\n {description}\n" \
               f"<b>Admin</b>: {admin.name}\n" \
               f"<b>Delay</b>: {delay.value} days\n" \
               f"<b>Show</b>: {ads.show}\n" \
               f"<b>Show in comment</b>: {ads.comment_add}"

        await state.clear()
        if str(media) == "":
            await query.message.answer(text, parse_mode="html", reply_markup=await cancel_admin_kb(admin))
        else:
            file = FSInputFile(media)
            if str(media).find("photo") != -1:
                await query.message.answer_photo(photo=file,
                                                 caption=text,
                                                 parse_mode="html",
                                                 reply_markup=await cancel_admin_kb(admin))
            elif str(media).find("video") != -1:
                await query.message.answer_video(video=file,
                                                 caption=text,
                                                 parse_mode="html",
                                                 reply_markup=await cancel_admin_kb(admin))
            elif str(media).find("gif") != -1:
                await query.message.answer_animation(animation=file,
                                                     caption=text,
                                                     parse_mode="html",
                                                     reply_markup=await cancel_admin_kb(admin))
            else:
                pass
    except Exception as e:
        logging.error(e)


@router.message(StateFilter(AddAdsState.ads_media),
                F.content_type.in_({ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION}))
async def add_photo_handler(message: Message, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        #
        if message.photo[-1].file_id:
            destination_path = f"app/media/admin/photo/{message.photo[-1].file_unique_id}.png"
            file_id = message.photo[-1].file_id
        elif message.video.file_id:
            file_id = message.video.file_id
            destination_path = f"app/media/admin/video/{message.video.file_unique_id}.mp4"
        elif message.animation.file_id:
            file_id = message.animation.file_id
            destination_path = f"app/media/admin/gif/{message.animation.file_unique_id}.gif.mp4"
        else:
            await state.set_state(AddAdsState.ads_media)
            await message.answer(
                text="Something's wrong resend media \n"
                     "it should be` photo, video(0-60 seconds), gif",
                reply_markup=await continue_admin_kb(data['admin']))
        file = await bot.get_file(file_id)

        file_save = await bot.download(file, destination_path)

        data['media'] = destination_path
        await state.set_data(data)
        await state.set_state(AddAdsState.ads_left_time)
        await message.answer("Now choose timedelay in which ads would be shown",
                             reply_markup=await ads_delay_admin_kb(data['admin']))
    except Exception as e:
        logging.error(e)


@router.message(IsOwnerFilter(), StateFilter(AddAdsState.ads_description))
async def ads_description_message(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        data['description'] = message.text
        await state.set_data(data)
        await state.set_state(AddAdsState.ads_media)
        await message.answer("Ok now send media of add\n"
                             "or press continue button",
                             reply_markup=await continue_admin_kb(data['admin']))

    except Exception as e:
        logging.error(e)


@router.message(IsOwnerFilter(), StateFilter(AddAdsState.ads_name))
async def ads_name_message(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        data['name'] = message.text
        await state.set_data(data)
        await state.set_state(AddAdsState.ads_description)
        await message.answer("Ok now send description of add\n"
                             "that user's will sea",
                             reply_markup=await cancel_admin_kb(data['admin']))

    except Exception as e:
        logging.error(e)


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.ADD_ADS))
async def add_admin_ads_cb(query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.user_id)
        await state.set_data({"admin": admin})
        await query.message.edit_text("Let's start adding\n"
                                      "What is ads name?")
        await query.message.edit_reply_markup(await cancel_admin_kb(admin))
        await state.set_state(AddAdsState.ads_name)
    except Exception as e:
        logging.error(e)
