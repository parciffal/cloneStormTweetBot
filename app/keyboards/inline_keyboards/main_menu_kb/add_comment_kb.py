from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from app.utils.callback_data.main_menu_cb_data import MenuActions, MainMenuCbData
from app.utils.callback_data.chg_comnt_cb_data import ChgCommentCbData, CommentActions


async def remove_comment_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Add comment",
                                 callback_data=ChgCommentCbData(
                                     action=CommentActions.CHANGE_COMMENT,
                                     user_id=group_id
                                 ).pack())
        ],
        [
            InlineKeyboardButton(text="Back to Menu",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.BACK_TO_MENU,
                                     user_id=group_id).pack()),

            InlineKeyboardButton(text="Finish",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.FINISH,
                                     user_id=group_id).pack())
        ]
    ]
    )


async def edit_comment_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Show comment",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.ADD_COMMENT,
                                     user_id=group_id
                                 ).pack())
        ],
        [
            InlineKeyboardButton(text="Back to Menu",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.BACK_TO_MENU,
                                     user_id=group_id).pack()),

            InlineKeyboardButton(text="Finish",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.FINISH,
                                     user_id=group_id).pack())
        ]
    ]
    )


async def change_comment_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Change comment",
                                 callback_data=ChgCommentCbData(
                                     action=CommentActions.CHANGE_COMMENT,
                                     user_id=group_id
                                 ).pack())
        ],
        [
            InlineKeyboardButton(text="Remove comment",
                                 callback_data=ChgCommentCbData(
                                     action=CommentActions.REMOVE_COMMENT,
                                     user_id=group_id
                                 ).pack())
        ],
        [
            InlineKeyboardButton(text="Back to Menu",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.BACK_TO_MENU,
                                     user_id=group_id).pack()),

            InlineKeyboardButton(text="Finish",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.FINISH,
                                     user_id=group_id).pack())
        ]
    ]
    )
