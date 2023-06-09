import aiofiles.os
from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType, FSInputFile

from app.keyboards.inline_keyboards.main_menu_kb import MenuActions, MainMenuCbData
from app.keyboards.inline_keyboards.main_menu_kb.show_media_kb import (ShowMediaCallback, MediaActions,
                                                                       show_media_kb, no_media_kb)
from app.utils.states.user_states import MediaState
from app.db.models import GroupModel
import logging
import aiofiles
import os
router = Router()


@router.message(StateFilter(MediaState.change_media),
                F.content_type.in_({ContentType.PHOTO}))
async def add_photo_handler(message: Message, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        group = await GroupModel.get(telegram_id=data['group_id'])
        #
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)

        # Specify the destination path to save the photo
        destination_path = f"app/media/photo/{message.photo[-1].file_unique_id}.png"
        file_save = await bot.download(file, destination_path)
        await state.clear()
        group.media = destination_path
        await group.save()
        await message.delete()
        await data["message"].delete()
        filw = FSInputFile(destination_path)
        await message.answer_photo(filw,
                                   caption="Image saved",
                                   reply_markup=await show_media_kb(group.telegram_id))
    except Exception as e:
        logging.error(e)


@router.message(StateFilter(MediaState.change_media),
                F.content_type.in_({ContentType.VIDEO}))
async def add_video_handler(message: Message, bot: Bot, state: FSMContext):
    logging.info(message.video.file_id)
    try:
        data = await state.get_data()
        group = await GroupModel.get(telegram_id=data['group_id'])
        #
        file_id = message.video.file_id
        file = await bot.get_file(file_id)

        # Specify the destination path to save the photo
        destination_path = f"app/media/video/{message.video.file_unique_id}.mp4"
        file_save = await bot.download(file, destination_path)
        await state.clear()
        group.media = destination_path
        await group.save()
        await message.delete()

        await data["message"].delete()
        filw = FSInputFile(destination_path)
        await message.answer_video(filw,
                                   caption="Video saved",
                                   reply_markup=await show_media_kb(group.telegram_id))
    except Exception as e:
        logging.error(e)


@router.message(StateFilter(MediaState.change_media),
                F.content_type.in_({ContentType.ANIMATION}))
async def add_animation_handler(message: Message, bot: Bot, state: FSMContext):
    logging.info(message.animation.file_id)
    try:
        data = await state.get_data()
        group = await GroupModel.get(telegram_id=data['group_id'])
        #
        file_id = message.animation.file_id
        file = await bot.get_file(file_id)

        # Specify the destination path to save the photo
        destination_path = f"app/media/gif/{message.animation.file_unique_id}.gif.mp4"
        file_save = await bot.download(file, destination_path)
        group.media = destination_path

        await state.clear()
        await group.save()
        await message.delete()
        await data["message"].delete()

        filw = FSInputFile(destination_path)

        await message.answer_animation(filw,
                                       caption="GIF saved",
                                       reply_markup=await show_media_kb(group.telegram_id))
    except Exception as e:
        logging.error(e)


@router.callback_query(ShowMediaCallback.filter(F.action == MediaActions.ADD))
async def add_media_cb(query: CallbackQuery, callback_data: ShowMediaCallback, state: FSMContext):
    try:
        await state.set_state(MediaState.change_media)
        await state.set_data({
            "group_id": callback_data.group_id,
            "message": query.message
        })
        await query.message.edit_text(
            "Please send an image, gif, or video or enter /cancel to abort")
    except Exception as e:
        logging.error(e)


@router.callback_query(ShowMediaCallback.filter(F.action == MediaActions.CHANGE))
async def change_media_cb(query: CallbackQuery, callback_data: ShowMediaCallback, state: FSMContext):
    try:
        await state.set_state(MediaState.change_media)
        await state.set_data({
            "group_id": callback_data.group_id,
            "message": query.message
        })

        await query.message.delete()
        await query.message.answer("Please send an image, gif, or video or enter /cancel to abort")

    except Exception as e:
        logging.error(e)


@router.callback_query(ShowMediaCallback.filter(F.action == MediaActions.REMOVE))
async def remove_media_cb(query: CallbackQuery, callback_data: ShowMediaCallback, state: FSMContext):
    try:

        group_id = callback_data.group_id
        group = await GroupModel.get(telegram_id=group_id)
        file_name = os.path.realpath(group.media)

        handle = await aiofiles.os.remove(file_name)
        group.media = ""
        await group.save()
        await query.message.delete()
        await query.message.answer("Media removed!", reply_markup=await no_media_kb(callback_data.group_id))
    except Exception as e:
        logging.error(e)


@router.callback_query(MainMenuCbData.filter(F.action == MenuActions.SHOW_MEDIA))
async def show_media_cb(query: CallbackQuery, callback_data: MainMenuCbData, state: FSMContext):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)

        if group.media == "":
            await query.message.edit_text("No media text")
            await query.message.edit_reply_markup(await no_media_kb(callback_data.group_id))
        else:
            filw = FSInputFile(group.media)
            await query.message.delete()
            if str(group.media).find("gif") != -1:
                await query.message.answer_animation(
                    filw,
                    caption="This media will be sent along with message in group!",
                    reply_markup=await show_media_kb(callback_data.group_id))
            elif str(group.media).find("photo") != -1:
                await query.message.answer_photo(
                    filw,
                    caption="This media will be sent along with message in group!",
                    reply_markup=await show_media_kb(callback_data.group_id))
            elif str(group.media).find("video") != -1:
                await query.message.answer_video(
                    filw,
                    caption="This media will be sent along with message in group!",
                    reply_markup=await show_media_kb(callback_data.group_id))
    except Exception as e:
        logging.error(e)
