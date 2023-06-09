from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, ContentType, FSInputFile
from aiogram.utils.text_decorations import html_decoration
from aiogram.fsm.context import FSMContext

from app.db.models import AdminModel, AdsModel
from app.keyboards.admin_inline_keyboards import cancel_admin_kb
from app.keyboards.admin_inline_keyboards.add_admin_ads_kb import ads_pagination
from app.keyboards.admin_inline_keyboards.view_ads_kb import ads_back_kb, ads_edit_kb
from app.utils.callback_data.admin_callback_data import AdsCB, AdsActions
from app.utils.callback_data.admin_callback_data.view_ads_cb import ViewAdsActions, ViewAdsCB
from app.utils.states.admin_states import EditAdsState

import logging


router = Router()


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_SHOW))
async def view_ads_chg_show(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        ads = await AdsModel.get(id=callback_data.ads_id)
        ads.show = not ads.show
        await ads.save()
        await view_ads_edit_cb(query, callback_data, state)
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_SHOW_IN_COM))
async def view_ads_chg_show_comm(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        ads = await AdsModel.get(id=callback_data.ads_id)
        ads.comment_add = not ads.comment_add
        await ads.save()
        await view_ads_edit_cb(query, callback_data, state)
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_MEDIA))
async def view_ads_chg_media(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        pass
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_DELAY))
async def view_ads_chg_delay(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        pass
    except Exception as e:
        logging.error(e)


@router.message(F.content_type.in_({ContentType.TEXT}), StateFilter(EditAdsState.ads_description))
async def view_ads_chg_desc_msg(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        ads = await AdsModel.get(id=data['ads_id'])
        ads.description = message.text
        await ads.save()
        await state.clear()

        admin = await AdminModel.get(telegram_id=ads.admin.telegrma_id)
        text = f"<b>Ads info</b>\n" \
               f"<b>Name</b>: {ads.name}\n" \
               f"<b>Description</b>:\n {ads.description}\n" \
               f"<b>Admin</b>: {admin.name}\n" \
               f"<b>Delay</b>: {ads.left_time} days\n" \
               f"<b>Show</b>: {ads.show}\n" \
               f"<b>Show in comment</b>: {ads.comment_add}"

        await message.delete()
        await state.clear()
        if str(ads.media) == "":
            await message.answer(text,
                                 parse_mode="html",
                                 reply_markup=await ads_back_kb(ads.id, admin))
        else:

            file = FSInputFile(ads.media)
            if str(ads.media).find("photo") != -1:
                await message.answer_photo(photo=file,
                                           caption=text,
                                           parse_mode="html",
                                           reply_markup=await ads_back_kb(ads.id, admin))
            elif str(ads.media).find("video") != -1:
                await message.answer_video(video=file,
                                           caption=text,
                                           parse_mode="html",
                                           reply_markup=await ads_back_kb(ads.id, admin))
            elif str(ads.media).find("gif") != -1:
                await message.answer_animation(animation=file,
                                               caption=text,
                                               parse_mode="html",
                                               reply_markup=await ads_back_kb(ads.id, admin))
            else:
                pass
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_DESC))
async def view_ads_chg_description(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        await state.set_state(EditAdsState.ads_description)
        data = await state.get_data()
        data['ads_id'] = callback_data.ads_id
        data['admin'] = callback_data.user_id
        await state.set_data(data)
        await query.message.delete()
        await query.message.answer("Send new description of ads or /cancel")
    except Exception as e:
        logging.error(e)


@router.message(F.content_type.in_({ContentType.TEXT}), StateFilter(EditAdsState.ads_name))
async def view_ads_chg_name_msg(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        ads = await AdsModel.get(id=data['ads_id'])
        ads.name = message.text
        await ads.save()
        await state.clear()
        admin = await AdminModel.get(telegram_id=ads.admin[0].telegram_id)
        text = f"<b>Ads info</b>\n" \
               f"<b>Name</b>: {ads.name}\n" \
               f"<b>Description</b>:\n {ads.description}\n" \
               f"<b>Admin</b>: {admin.name}\n" \
               f"<b>Delay</b>: {ads.left_time} days\n" \
               f"<b>Show</b>: {ads.show}\n" \
               f"<b>Show in comment</b>: {ads.comment_add}"

        await message.delete()
        await state.clear()
        if str(ads.media) == "":
            await message.answer(text,
                                 parse_mode="html",
                                 reply_markup=await ads_back_kb(ads.id, admin))
        else:

            file = FSInputFile(ads.media)
            if str(ads.media).find("photo") != -1:
                await message.answer_photo(photo=file,
                                           caption=text,
                                           parse_mode="html",
                                           reply_markup=await ads_back_kb(ads.id, admin))
            elif str(ads.media).find("video") != -1:
                await message.answer_video(video=file,
                                           caption=text,
                                           parse_mode="html",
                                           reply_markup=await ads_back_kb(ads.id, admin))
            elif str(ads.media).find("gif") != -1:
                await message.answer_animation(animation=file,
                                               caption=text,
                                               parse_mode="html",
                                               reply_markup=await ads_back_kb(ads.id, admin))
            else:
                pass
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_NAME))
async def view_ads_chg_name(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        await state.set_state(EditAdsState.ads_name)
        data = await state.get_data()
        data['ads_id'] = callback_data.ads_id
        data['admin'] = callback_data.user_id
        await state.set_data(data)
        await query.message.delete()
        await query.message.answer("Send new name of ads or /cancel")
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.BACK_TO_ADD))
async def view_ads_back_to_ads(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.user_id)
        await query.message.edit_reply_markup(await ads_back_kb(callback_data.ads_id, admin))

    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.EDIT))
async def view_ads_edit_cb(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.user_id)
        keyboard = await ads_edit_kb(callback_data.ads_id, admin)
        ads = await AdsModel.get(id=callback_data.ads_id)
        text = f"<b>Ads info</b>\n" \
               f"<b>Name</b>: {ads.name}\n" \
               f"<b>Description</b>:\n {ads.description}\n" \
               f"<b>Admin</b>: {admin.name}\n" \
               f"<b>Delay</b>: {ads.left_time} days\n" \
               f"<b>Show</b>: {ads.show}\n" \
               f"<b>Show in comment</b>: {ads.comment_add}"
        try:
            await query.message.edit_text(text, parse_mode="html")
        except:
            await query.message.edit_caption(text, parse_mode="html")
        await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.BACK))
async def view_ads_back_cb(query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.user_id)
        try:
            data = await state.get_data()
            data['admin'] = admin
            await state.set_data(data)
            page = await ads_pagination(admin, data['page'])
        except:
            await state.set_data({"admin": admin})
            page = await ads_pagination(admin)
        await query.message.delete()
        await query.message.answer(text="Choose ads to edit", parse_mode="html", reply_markup=page)
    except Exception as e:
        logging.error(e)


@router.callback_query(AdsCB.filter(F.action == AdsActions.SHOW_ADS))
async def view_ads_cb(query: CallbackQuery, callback_data: AdsCB, state: FSMContext):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.user_id)
        ads = await AdsModel.get(id=callback_data.ads_id, admin=admin)
        text = f"<b>Ads info</b>\n" \
               f"<b>Name</b>: {ads.name}\n" \
               f"<b>Description</b>:\n {ads.description}\n" \
               f"<b>Admin</b>: {admin.name}\n" \
               f"<b>Delay</b>: {ads.left_time} days\n" \
               f"<b>Show</b>: {ads.show}\n" \
               f"<b>Show in comment</b>: {ads.comment_add}"

        await state.clear()
        if str(ads.media) == "":
            await query.message.delete()
            await query.message.answer(text,
                                       parse_mode="html",
                                       reply_markup=await ads_back_kb(callback_data.ads_id, admin))
        else:

            file = FSInputFile(ads.media)
            if str(ads.media).find("photo") != -1:
                await query.message.delete()
                await query.message.answer_photo(photo=file,
                                                 caption=text,
                                                 parse_mode="html",
                                                 reply_markup=await ads_back_kb(callback_data.ads_id, admin))
            elif str(ads.media).find("video") != -1:
                await query.message.delete()
                await query.message.answer_video(video=file,
                                                 caption=text,
                                                 parse_mode="html",
                                                 reply_markup=await ads_back_kb(callback_data.ads_id, admin))
            elif str(ads.media).find("gif") != -1:
                await query.message.delete()
                await query.message.answer_animation(animation=file,
                                                     caption=text,
                                                     parse_mode="html",
                                                     reply_markup=await ads_back_kb(callback_data.ads_id, admin))
            else:
                pass
    except Exception as e:
        logging.error(e)
