from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from app.utils.callback_data.main_menu_cb_data import MenuActions, MainMenuCbData


async def main_menu_kb(user_data: dict) -> InlineKeyboardMarkup:
    """
    :param user_data: {
        "group_id": group.telegram_id,
        "raid_msg": group.influencers_tweets,
        "retweets/replies": group.retweets_replies,
        "comment_raid_msg": True if group.comments else False,
        "current_comment": group.comments if group.comments else "No comment",
        "templates_count": len(template_count),
        "delay": group.delay,
        "account_count": len(account_count)
    }

    :return: Main menu keyboard
    """
    raid_btn_txt = "❌ Influencers Tweets"
    comment_raid_btn_txt = "❌ Retweets/Replies"

    if user_data['raid_msg']:
        raid_btn_txt = "✅ Influencers Tweets"

    if user_data['retweets/replies']:
        comment_raid_btn_txt = "✅ Retweets/Replies"

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=raid_btn_txt,
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.CH_INF_TWEETS,
                                     group_id=user_data['group_id']).pack()),
            InlineKeyboardButton(text=comment_raid_btn_txt,
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.RETWEETS_REPLIES,
                                     group_id=user_data['group_id']).pack())
        ],
        [
            InlineKeyboardButton(text="Custom comment",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.ADD_COMMENT,
                                     group_id=user_data['group_id']).pack()),
            InlineKeyboardButton(text="Set Template",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.SET_TEMPLATE,
                                     group_id=user_data['group_id']).pack())
        ],
        [
            InlineKeyboardButton(text="Change delay",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.CHANGE_DELAY,
                                     group_id=user_data['group_id']).pack()),
            InlineKeyboardButton(text="Show media",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.SHOW_MEDIA,
                                     group_id=user_data['group_id']).pack())
        ],
        [
            InlineKeyboardButton(text="➕ account",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.ADD_ACCOUNT,
                                     group_id=user_data['group_id']).pack()),
            InlineKeyboardButton(text="Finish",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.FINISH,
                                     group_id=user_data['group_id']).pack())
        ]
    ])
    return markup


async def return_kb(group_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Back to Menu",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.BACK_TO_MENU,
                                     group_id=group_id).pack()),
        ],
        [
            InlineKeyboardButton(text="Finish",
                                 callback_data=MainMenuCbData(
                                     action=MenuActions.FINISH,
                                     group_id=group_id).pack())
        ]
    ]
    )
